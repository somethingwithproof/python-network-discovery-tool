"""Host discovery and service checks.

The default backend uses plain asyncio sockets: TCP connects and an SNMPv3
discovery datagram, so it needs neither nmap nor root. The optional nmap
backend only replaces host discovery with an nmap ping sweep, which can find
hosts that expose none of the probed ports.
"""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import re
import socket
from collections.abc import Iterable
from typing import Any, Literal

from rich.progress import Progress

from netprobe.config import DEFAULT_SERVICES
from netprobe.models import LEGACY_FLAGS, Device, Service, ServiceSpec
from netprobe.probes import PROBES, ProbeContext, ProbeResult, SnmpCredentials

logger = logging.getLogger(__name__)

Backend = Literal["asyncio", "nmap"]

# Largest network accepted in one run. A /8 would otherwise queue 16M scan tasks.
MAX_HOSTS = 65536
# Per-nmap-invocation cap so one unresponsive host cannot hang a sweep.
NMAP_HOST_TIMEOUT = "30s"
DEFAULT_TIMEOUT = 1.0
DEFAULT_CONCURRENCY = 256
# Every socket in flight is a file descriptor.
MAX_CONCURRENCY = 4096
# Hosts x services in one run, so --ports and the config cannot multiply a
# /16 into millions of probes.
MAX_PROBES = 524288
# A probe may connect twice (HTTPS retry) and read once; this is its hard
# ceiling in units of --timeout, so no single probe can stall a scan.
PROBE_BUDGET = 4
HOSTNAME_TIMEOUT = 2.0


_HOSTNAME_LABEL = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")


class BackendUnavailableError(RuntimeError):
    """The requested backend cannot run on this machine."""


def validate_target(target: str) -> str:
    """Return target if it is an IP address or a DNS name, else raise ValueError.

    The nmap backend passes the value to the nmap command line, so anything
    that could be read as an option (leading "-") or contains whitespace is
    rejected for every backend.
    """
    try:
        return str(ipaddress.ip_address(target))
    except ValueError:
        pass

    labels = target.split(".")
    # A purely numeric last label means a malformed IPv4 address, not a hostname.
    if (
        len(target) > 253
        or not all(_HOSTNAME_LABEL.match(label) for label in labels)
        or labels[-1].isdigit()
    ):
        raise ValueError(f"Invalid target: {target!r}")
    return target


def expand_targets(network: str) -> list[str]:
    """Expand a CIDR, IP or hostname into the list of hosts to scan."""
    try:
        if "/" in network:
            net = ipaddress.ip_network(network, strict=False)
            if net.num_addresses > MAX_HOSTS:
                raise ValueError(
                    f"Network too large: {net.num_addresses} addresses (max {MAX_HOSTS})"
                )
            return [str(ip) for ip in net.hosts()]
        return [validate_target(network)]
    except ValueError as e:
        raise ValueError(f"Invalid network format: {e}") from e


def _host_key(hosts: list[str], target: str) -> str | None:
    """Find the result entry for target; nmap keys results by IP, not hostname."""
    if target in hosts:
        return target
    try:
        ipaddress.ip_address(target)
    except ValueError:
        return hosts[0] if len(hosts) == 1 else None
    return None


def _nmap_scanner() -> Any:
    try:
        import nmap
    except ImportError as e:
        raise BackendUnavailableError(
            "the nmap backend needs python-nmap: pip install 'netprobe[nmap]'"
        ) from e
    try:
        return nmap.PortScanner()
    except nmap.PortScannerError as e:
        raise BackendUnavailableError(f"nmap is not available: {e}") from e


def nmap_sweep(targets: list[str], network: str) -> set[str]:
    """Return the targets that answer an nmap ping sweep.

    Without root, nmap substitutes TCP connects to ports 80 and 443 for ICMP.
    """
    nm = _nmap_scanner()
    arguments = f"-sn -T4 --host-timeout {NMAP_HOST_TIMEOUT}"
    nm.scan(hosts=network if "/" in network else targets[0], arguments=arguments)
    up = [h for h in nm.all_hosts() if nm[h].state() == "up"]
    if "/" in network:
        return set(up)
    return {targets[0]} if _host_key(up, targets[0]) else set()


async def resolve_hostname(ip: str) -> str:
    try:
        async with asyncio.timeout(HOSTNAME_TIMEOUT):
            name, _, _ = await asyncio.to_thread(socket.gethostbyaddr, ip)
    except (TimeoutError, OSError) as e:
        logger.debug(f"Could not resolve hostname for {ip}: {e}")
        return ""
    return name


class NetworkScanner:
    """Async network scanner."""

    def __init__(
        self,
        *,
        backend: Backend = "asyncio",
        timeout: float = DEFAULT_TIMEOUT,
        concurrency: int = DEFAULT_CONCURRENCY,
        services: Iterable[ServiceSpec] = DEFAULT_SERVICES,
        snmp: SnmpCredentials | None = None,
        tls_ca_file: str | None = None,
    ) -> None:
        if not 1 <= concurrency <= MAX_CONCURRENCY:
            raise ValueError(f"concurrency must be from 1 to {MAX_CONCURRENCY}")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.backend = backend
        self.timeout = timeout
        self.concurrency = concurrency
        self.services = tuple(services)
        self.context = ProbeContext(timeout=timeout, snmp=snmp, tls_ca_file=tls_ca_file)
        if snmp is not None:
            # Load pysnmp now; its first import takes about a second and would
            # otherwise count against the first SNMP probe's time budget.
            import pysnmp.hlapi.v3arch.asyncio  # noqa: F401
        if backend == "nmap":
            # Fail before any scanning starts if nmap cannot be driven.
            _nmap_scanner()

    async def scan_device(
        self, ip: str, *, probes: asyncio.Semaphore | None = None, known_up: bool = False
    ) -> Device:
        """Probe every configured service on one host.

        Args:
            ip: IP address or hostname to scan
            probes: shared limit on probes in flight across hosts
            known_up: host discovery already saw the host, even if no probe answers

        Returns:
            Device object with scan results
        """
        device = Device(ip=ip)
        try:
            validate_target(ip)
        except ValueError as e:
            device.errors.append(str(e))
            return device

        limit = probes or asyncio.Semaphore(self.concurrency)

        async def run(spec: ServiceSpec) -> Service:
            async with limit:
                try:
                    probe, _ = PROBES[spec.probe]
                    async with asyncio.timeout(self.timeout * PROBE_BUDGET):
                        result = await probe(ip, spec.port, self.context)
                except TimeoutError:
                    device.errors.append(f"Error checking port {spec.port}: probe timed out")
                    result = ProbeResult("filtered")
                except Exception as e:
                    message = str(e)
                    if self.context.snmp:
                        message = self.context.snmp.redact(message)
                    device.errors.append(f"Error checking port {spec.port}: {message}")
                    result = ProbeResult("filtered")
            return Service(
                spec.name, spec.port, spec.protocol, result.state, result.version, result.details
            )

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(run(spec)) for spec in self.services]

        device.services = [t.result() for t in tasks]
        open_names = {s.name for s in device.open_services}
        for flag in LEGACY_FLAGS:
            setattr(device, flag, flag in open_names)
        device.alive = known_up or any(s.state != "filtered" for s in device.services)
        if device.alive:
            device.hostname = await resolve_hostname(ip)
        else:
            device.errors.append("Host is down")
        return device

    async def scan_network(self, network: str, progress: Progress | None = None) -> list[Device]:
        """Scan an entire network.

        Args:
            network: Network in CIDR notation (e.g., "192.168.1.0/24"), IP, or hostname
            progress: Optional Rich progress bar

        Returns:
            List of scanned devices, in address order

        Raises:
            ValueError: if the target is malformed or larger than MAX_HOSTS
        """
        targets = expand_targets(network)
        probes_needed = len(targets) * len(self.services)
        if probes_needed > MAX_PROBES:
            raise ValueError(
                f"Scan too large: {len(targets)} hosts x {len(self.services)} services = "
                f"{probes_needed} probes (max {MAX_PROBES}); narrow the range or the services"
            )
        logger.info(f"Scanning {len(targets)} hosts...")
        task = (
            progress.add_task("[cyan]Scanning network...", total=len(targets)) if progress else None
        )

        swept: set[str] | None = None
        if self.backend == "nmap":
            swept = await asyncio.to_thread(nmap_sweep, targets, network)

        probes = asyncio.Semaphore(self.concurrency)
        # Bounds hosts in flight so a /16 does not hold 65k sockets' worth of tasks.
        hosts = asyncio.Semaphore(max(1, self.concurrency // max(1, len(self.services))))

        async def scan_one(ip: str) -> Device:
            async with hosts:
                if swept is not None and ip not in swept:
                    device = Device(ip=ip, errors=["Host is down"])
                else:
                    device = await self.scan_device(ip, probes=probes, known_up=swept is not None)
            if progress and task is not None:
                progress.update(task, advance=1)
            return device

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(scan_one(ip)) for ip in targets]

        return [t.result() for t in tasks]
