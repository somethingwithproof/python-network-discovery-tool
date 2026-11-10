# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Host discovery and service checks.

The default backend uses plain asyncio sockets: TCP connects and an SNMPv3
discovery datagram, so it needs neither nmap nor root. The optional nmap
backend only replaces host discovery with an nmap ping sweep, which can find
hosts that expose none of the probed ports.
"""

from __future__ import annotations

import asyncio
import contextlib
import ipaddress
import logging
import math
import re
import shutil
import socket
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import replace
from typing import Literal

from defusedxml.ElementTree import ParseError, fromstring
from rich.progress import Progress, TaskID

from netprobe.config import DEFAULT_SERVICES
from netprobe.models import LEGACY_FLAGS, Device, Service, ServiceSpec
from netprobe.probes import PROBES, ProbeContext, ProbeResult, SnmpCredentials, clean

logger = logging.getLogger(__name__)

Backend = Literal["asyncio", "nmap"]

# Largest network accepted in one run. A /8 would otherwise queue 16M scan tasks.
MAX_HOSTS = 65536
# Per-host cap inside nmap so one unresponsive host cannot hang a sweep.
NMAP_HOST_TIMEOUT = "30s"
# One nmap process for a full prefix. The subprocess deadline grows by this
# much for every NMAP_BATCH addresses, which matches the old per-batch ceiling.
NMAP_BATCH = 256
NMAP_TIMEOUT = 35
# XML for a /16 of live hosts is a few tens of MB; refuse anything larger.
NMAP_MAX_OUTPUT = 64 * 1024 * 1024
DEFAULT_TIMEOUT = 1.0
# The CLI's whole-scan limit, nmap sweep included. A /16 at the default
# concurrency finishes well inside it; a stalled network does not run forever.
DEFAULT_DEADLINE = 3600.0
MAX_DEADLINE = 7 * 24 * 3600.0
DEFAULT_CONCURRENCY = 256
# Every socket in flight is a file descriptor.
MAX_CONCURRENCY = 4096
# Hosts x services in one run, so --ports and the config cannot multiply a
# /16 into millions of probes.
MAX_PROBES = 524288
# A probe may connect twice (HTTPS retry) and read once; this is its hard
# ceiling in units of that probe's own timeout.
PROBE_BUDGET = 4
HOSTNAME_TIMEOUT = 2.0
SCOPE_ERROR = "IPv6 scope identifiers are not supported"
HOST_DOWN = "Host is down"
# Port states that prove something on the host answered.
ANSWERED = frozenset({"open", "closed"})
# File descriptors kept free for stdio, logging, pysnmp and the event loop.
FD_HEADROOM = 64


# Applied with fullmatch: "$" with match() also accepts a trailing newline.
_HOSTNAME_LABEL = re.compile(r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)")
# Reverse DNS names in the wild also use underscores.
_PTR_NAME = re.compile(r"\w(?:[\w.-]{0,251}\w)?", re.ASCII)
# Concurrent forward and reverse lookups; each occupies a resolver thread.
DNS_CONCURRENCY = 16


class BackendUnavailableError(RuntimeError):
    """The requested backend cannot run on this machine."""


def validate_target(target: str) -> str:
    """Return target if it is an IP address or a DNS name, else raise ValueError.

    The nmap backend passes the value to the nmap command line, so anything
    that could be read as an option (leading "-") or contains whitespace is
    rejected for every backend.
    """
    if "%" in target:
        raise ValueError(SCOPE_ERROR)
    try:
        return str(ipaddress.ip_address(target))
    except ValueError:
        pass

    labels = target.split(".")
    # A purely numeric last label means a malformed IPv4 address, not a hostname.
    if (
        len(target) > 253
        or not all(_HOSTNAME_LABEL.fullmatch(label) for label in labels)
        or labels[-1].isdigit()
    ):
        raise ValueError(f"Invalid target: {target!r}")
    return target


type Address = ipaddress.IPv4Address | ipaddress.IPv6Address
type Network = ipaddress.IPv4Network | ipaddress.IPv6Network

_MAPPED = ipaddress.IPv6Network("::ffff:0:0/96")
# RFC 6052 well-known prefix: a NAT64 gateway forwards these to the embedded IPv4.
_NAT64 = ipaddress.IPv6Network("64:ff9b::/96")


def canonical_network(value: str) -> Network:
    """Parse a prefix, rewriting IPv4-mapped IPv6 as the IPv4 range it denotes.

    The socket layer sends ::ffff:a.b.c.d to a.b.c.d over IPv4, so both
    spellings must expand, exclude and compare as one host.
    """
    network = ipaddress.ip_network(value, strict=False)
    if isinstance(network, ipaddress.IPv6Network) and network.subnet_of(_MAPPED):
        mapped = int(network.network_address) & 0xFFFFFFFF
        return ipaddress.IPv4Network((mapped, network.prefixlen - 96))
    return network


def _canonical(target: str) -> str:
    """An IP target in canonical form, IPv4-mapped IPv6 as IPv4; names unchanged."""
    try:
        return str(canonical_network(target).network_address)
    except ValueError:
        return target


def _aliases(address: Address) -> list[Address]:
    """Every spelling that reaches this host: itself, its IPv4-mapped form, or the
    IPv4 address a 6to4 or NAT64 address embeds."""
    if isinstance(address, ipaddress.IPv4Address):
        return [address, ipaddress.IPv6Address(int(_MAPPED.network_address) | int(address))]
    if address in _NAT64:
        return [address, ipaddress.IPv4Address(int(address) & 0xFFFFFFFF)]
    return [address] if address.sixtofour is None else [address, address.sixtofour]


def _excluded(address: Address, blocked: list[Network]) -> bool:
    return any(alias in net for alias in _aliases(address) for net in blocked)


def expand_targets(
    network: str, max_hosts: int = MAX_HOSTS, exclusions: Iterable[str] = ()
) -> list[str]:
    """Bound expansion before filtering; exclusions never justify expanding a huge range."""
    try:
        if type(max_hosts) is not int or not 1 <= max_hosts <= MAX_HOSTS:
            raise ValueError(f"host limit must be from 1 to {MAX_HOSTS}")
        if "%" in network:
            raise ValueError(SCOPE_ERROR)
        if "/" in network:
            net = canonical_network(network)
            if net.num_addresses > max_hosts:
                raise ValueError(
                    f"Network too large: {net.num_addresses} addresses (max {max_hosts})"
                )
            targets = [str(ip) for ip in net.hosts()]
        else:
            targets = [_canonical(validate_target(network))]
        blocked = []
        for value in exclusions:
            if "%" in value:
                raise ValueError(SCOPE_ERROR)
            blocked.append(canonical_network(value))
        if blocked:
            try:
                addresses = [ipaddress.ip_address(target) for target in targets]
            except ValueError as exc:
                raise ValueError("IP exclusions require an IP or CIDR target") from exc
            targets = [str(ip) for ip in addresses if not _excluded(ip, blocked)]
        if not targets:
            raise ValueError("No targets remain after exclusions")
        return targets
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


def _nmap_executable() -> str:
    """Absolute path of the nmap executable on PATH."""
    executable = shutil.which("nmap")
    if executable is None:
        raise BackendUnavailableError("nmap is not available: no nmap executable on PATH")
    return executable


def parse_nmap_hosts(document: bytes) -> list[str]:
    """Addresses of hosts nmap's XML output reports as up.

    defusedxml refuses entity expansion and external references, so a
    malformed or hostile document fails instead of exhausting memory.
    """
    try:
        root = fromstring(document)
    except (ParseError, ValueError) as e:
        raise BackendUnavailableError(f"Nmap discovery failed: unreadable XML ({e})") from e
    up: list[str] = []
    for host in root.iter("host"):
        status = host.find("status")
        if status is None or status.get("state") != "up":
            continue
        addresses = [
            a.get("addr", "")
            for a in host.findall("address")
            if a.get("addrtype") in ("ipv4", "ipv6")
        ]
        up.extend(addresses[:1])
    return up


async def _read_bounded(stream: asyncio.StreamReader, limit: int) -> bytes:
    chunks: list[bytes] = []
    size = 0
    while chunk := await stream.read(65536):
        size += len(chunk)
        if size > limit:
            raise ValueError(f"output exceeded {limit} bytes")
        chunks.append(chunk)
    return b"".join(chunks)


async def _run_nmap(executable: str, hosts: list[str], ipv6: bool, deadline: float) -> list[str]:
    """Run one ping sweep and return the addresses that answered.

    The argv is fixed apart from targets, which validate_target already
    restricted to addresses, prefixes and DNS names; no shell is involved.
    """
    options = ["-6"] if ipv6 else []
    options += ["-sn", "-T4", "--host-timeout", NMAP_HOST_TIMEOUT, "-oX", "-"]
    try:
        async with asyncio.timeout(deadline):
            process = await asyncio.create_subprocess_exec(
                executable,
                *options,
                *hosts,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
            )
            try:
                if process.stdout is None:  # pragma: no cover - PIPE always sets it
                    raise ValueError("no output stream")
                output = await _read_bounded(process.stdout, NMAP_MAX_OUTPUT)
                status = await process.wait()
            finally:
                if process.returncode is None:
                    process.kill()
                    await process.wait()
    except TimeoutError as e:
        raise BackendUnavailableError(
            f"Nmap discovery failed: no result within {deadline:g}s"
        ) from e
    except (OSError, ValueError) as e:
        raise BackendUnavailableError(f"Nmap discovery failed: {e}") from e
    if status != 0:
        raise BackendUnavailableError(f"Nmap discovery failed: nmap exited with status {status}")
    return parse_nmap_hosts(output)


def nmap_deadline(host_count: int) -> int:
    """Subprocess deadline for one nmap process covering host_count addresses."""
    batches = max(1, math.ceil(host_count / NMAP_BATCH))
    return NMAP_TIMEOUT * batches


async def nmap_sweep(targets: list[str], network: str) -> set[str]:
    """Return the targets that answer an nmap ping sweep.

    Without root, nmap substitutes TCP connects to ports 80 and 443 for ICMP.
    A full prefix is one process. Exclusions and partial lists stay in batches
    of NMAP_BATCH, each with a fixed NMAP_TIMEOUT deadline.
    """
    executable = _nmap_executable()
    ipv6 = all(":" in target for target in targets)
    batches: list[tuple[list[str], float]]
    if "/" in network and targets == expand_targets(network):
        batches = [([network], nmap_deadline(len(targets)))]
    else:
        batches = [
            (targets[index : index + NMAP_BATCH], NMAP_TIMEOUT)
            for index in range(0, len(targets), NMAP_BATCH)
        ]
    up: list[str] = []
    for hosts, deadline in batches:
        up.extend(await _run_nmap(executable, hosts, ipv6, deadline))
    if "/" in network:
        return set(up)
    return {targets[0]} if _host_key(up, targets[0]) else set()


def ensure_file_limit(concurrency: int) -> None:
    """Make room for one socket per in-flight probe, or refuse to start.

    macOS defaults to a 256-descriptor soft limit, the same as the default
    concurrency. Raise the soft limit toward the hard limit when needed.
    """
    try:
        import resource
    except ImportError:  # pragma: no cover - Windows has no RLIMIT_NOFILE
        return
    needed = concurrency + FD_HEADROOM
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    if soft == resource.RLIM_INFINITY or soft >= needed:
        return
    target = needed if hard == resource.RLIM_INFINITY else min(needed, hard)
    if target > soft:
        with contextlib.suppress(ValueError, OSError):
            resource.setrlimit(resource.RLIMIT_NOFILE, (target, hard))
            soft = target
    if soft < needed:
        raise ValueError(
            f"--concurrency {concurrency} needs {needed} open files but the limit is {soft}; "
            f"lower --concurrency or raise the limit (ulimit -n)"
        )


async def _lookup[T](slots: asyncio.Semaphore | None, start: Callable[[], Awaitable[T]]) -> T:
    """Run one resolver call in a lookup slot, giving up after HOSTNAME_TIMEOUT.

    The deadline starts once a slot is free, so a long queue does not expire
    lookups that never ran. The slot is freed when the resolver thread
    finishes rather than when the caller stops waiting, so lookups that
    outlive their deadline still count toward the limit.
    """
    slots = slots or asyncio.Semaphore(1)
    await slots.acquire()
    try:
        lookup = asyncio.ensure_future(start())
    except BaseException:
        slots.release()
        raise

    def finished(done: asyncio.Future[T]) -> None:
        slots.release()
        if not done.cancelled():
            done.exception()  # retrieved, so an abandoned failure is not logged

    lookup.add_done_callback(finished)
    async with asyncio.timeout(HOSTNAME_TIMEOUT):
        return await asyncio.shield(lookup)


async def resolve_hostname(ip: str, lookups: asyncio.Semaphore | None = None) -> str:
    """Reverse DNS name for ip, or "" when there is none or it is not a plain name.

    PTR data comes from whoever controls the reverse zone, so a name with
    anything but hostname characters is dropped rather than printed.
    """
    try:
        name, _, _ = await _lookup(lookups, lambda: asyncio.to_thread(socket.gethostbyaddr, ip))
    except OSError as e:
        logger.debug(f"Could not resolve hostname for {ip}: {e}")
        return ""
    name = name.rstrip(".")
    return name if _PTR_NAME.fullmatch(name) else ""


async def resolve_address(
    target: str, lookups: asyncio.Semaphore | None = None
) -> tuple[str, str | None]:
    """Return (address to probe, DNS name or None) for an IP or a hostname.

    A hostname is resolved once per host so every probe reaches the same
    address; resolving per connection would let round-robin or rebinding
    DNS answers send probes for one host to different machines.
    """
    try:
        return str(ipaddress.ip_address(target)), None
    except ValueError:
        pass
    loop = asyncio.get_running_loop()
    infos = await _lookup(lookups, lambda: loop.getaddrinfo(target, None, type=socket.SOCK_STREAM))
    if not infos:
        raise OSError(f"no address for {target}")
    return str(infos[0][4][0]), target


class ScanDeadlineError(Exception):
    """The whole scan ran past its deadline; ``devices`` holds the hosts that finished."""

    def __init__(self, devices: list[Device], deadline: float) -> None:
        super().__init__(f"scan stopped at its {deadline:g}s deadline")
        self.devices = devices
        self.deadline = deadline


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
        max_hosts: int = MAX_HOSTS,
        exclusions: Iterable[str] = (),
        deadline: float | None = None,
    ) -> None:
        if not 1 <= concurrency <= MAX_CONCURRENCY:
            raise ValueError(f"concurrency must be from 1 to {MAX_CONCURRENCY}")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be positive")
        if not 1 <= max_hosts <= MAX_HOSTS:
            raise ValueError(f"host limit must be from 1 to {MAX_HOSTS}")
        if deadline is not None and (not math.isfinite(deadline) or deadline <= 0):
            raise ValueError("deadline must be positive")
        self.deadline = deadline
        self.max_hosts = max_hosts
        self.exclusions = tuple(exclusions)
        self.backend = backend
        self.timeout = timeout
        self.concurrency = concurrency
        self.services = tuple(services)
        for spec in self.services:
            if spec.timeout is not None and (not math.isfinite(spec.timeout) or spec.timeout <= 0):
                raise ValueError(f"timeout for {spec.name} must be positive")
        self.context = ProbeContext(timeout=timeout, snmp=snmp, tls_ca_file=tls_ca_file)
        if snmp is not None:
            # Load pysnmp now; its first import takes about a second and would
            # otherwise count against the first SNMP probe's time budget.
            import pysnmp.hlapi.v3arch.asyncio  # noqa: F401
        if backend == "nmap":
            # Fail before any scanning starts if nmap cannot be driven.
            _nmap_executable()

    async def scan_device(
        self,
        ip: str,
        *,
        probes: asyncio.Semaphore | None = None,
        known_up: bool = False,
        lookups: asyncio.Semaphore | None = None,
    ) -> Device:
        """Probe every configured service on one host.

        Args:
            ip: IP address or hostname to scan
            probes: shared limit on probes in flight across hosts
            known_up: host discovery already saw the host, even if no probe answers
            lookups: shared limit on DNS lookups in flight across hosts

        Returns:
            Device object with scan results
        """
        device = Device(ip=ip)
        try:
            validate_target(ip)
        except ValueError as e:
            device.errors.append(str(e))
            return device

        try:
            address, server_name = await resolve_address(ip, lookups)
        except OSError as e:
            device.errors.append(f"Cannot resolve {ip}: {clean(str(e)) or type(e).__name__}")
            device.services = [
                Service(s.name, s.port, s.protocol, "unknown") for s in self.services
            ]
            return device
        device.address = address

        limit = probes or asyncio.Semaphore(self.concurrency)
        tasks: list[asyncio.Task[Service]] = []
        async with asyncio.TaskGroup() as tg:
            for spec in self.services:
                tasks.append(tg.create_task(self._probe(address, server_name, spec, limit, device)))

        device.services = [t.result() for t in tasks]
        open_names = {s.name for s in device.open_services}
        for flag in LEGACY_FLAGS:
            setattr(device, flag, flag in open_names)
        # Only an answer proves the host is up. A probe that failed locally or
        # hit its deadline says nothing, so such a host is not reported down.
        device.alive = known_up or any(s.state in ANSWERED for s in device.services)
        if device.alive:
            device.hostname = await resolve_hostname(address, lookups)
        elif all(s.state == "filtered" for s in device.services):
            device.errors.append(HOST_DOWN)
        return device

    async def _probe(
        self,
        address: str,
        server_name: str | None,
        spec: ServiceSpec,
        limit: asyncio.Semaphore,
        device: Device,
    ) -> Service:
        budget = self.timeout if spec.timeout is None else spec.timeout
        context = replace(self.context, timeout=budget, server_name=server_name)
        async with limit:
            try:
                probe, _ = PROBES[spec.probe]
                async with asyncio.timeout(budget * PROBE_BUDGET):
                    result = await probe(address, spec.port, context)
            except TimeoutError:
                device.errors.append(f"Error checking port {spec.port}: probe timed out")
                result = ProbeResult("unknown")
            except Exception as e:
                message = str(e) or type(e).__name__
                if self.context.snmp:
                    message = self.context.snmp.redact(message)
                device.errors.append(f"Error checking port {spec.port}: {message}")
                result = ProbeResult("unknown")
        return Service(
            spec.name, spec.port, spec.protocol, result.state, result.version, result.details
        )

    async def scan_network(self, network: str, progress: Progress | None = None) -> list[Device]:
        """Scan an entire network.

        Args:
            network: Network in CIDR notation (e.g., "192.168.1.0/24"), IP, or hostname
            progress: Optional Rich progress bar

        Returns:
            List of scanned devices, in address order

        Raises:
            ValueError: if the target is malformed or larger than MAX_HOSTS
            ScanDeadlineError: the scan, including any nmap sweep, outlasted
                the deadline; it carries the hosts that finished, in address order
        """
        targets = expand_targets(network, self.max_hosts, self.exclusions)
        probes_needed = len(targets) * len(self.services)
        if probes_needed > MAX_PROBES:
            raise ValueError(
                f"Scan too large: {len(targets)} hosts x {len(self.services)} services = "
                f"{probes_needed} probes (max {MAX_PROBES}); narrow the range or the services"
            )
        ensure_file_limit(self.concurrency)
        logger.info(f"Scanning {len(targets)} hosts...")
        task = (
            progress.add_task("[cyan]Scanning network...", total=len(targets)) if progress else None
        )

        results: list[Device | None] = [None] * len(targets)
        limit = asyncio.timeout(self.deadline)
        try:
            async with limit:
                await self._scan_targets(network, targets, results, progress, task)
        except TimeoutError:
            if not limit.expired():
                raise
            # Cancelling the workers stops their probes and any nmap process.
            finished = [device for device in results if device is not None]
            raise ScanDeadlineError(finished, self.deadline or 0) from None
        if any(device is None for device in results):
            raise asyncio.CancelledError("Inventory worker cancelled before completion")
        return [device for device in results if device is not None]

    async def _scan_targets(
        self,
        network: str,
        targets: list[str],
        results: list[Device | None],
        progress: Progress | None,
        task: TaskID | None,
    ) -> None:
        swept: set[str] | None = None
        if self.backend == "nmap":
            swept = await nmap_sweep(targets, network)

        probes = asyncio.Semaphore(self.concurrency)
        lookups = asyncio.Semaphore(DNS_CONCURRENCY)
        pending = iter(enumerate(targets))

        async def worker() -> None:
            for index, ip in pending:
                device = await self._scan_target(ip, swept, probes, lookups)
                results[index] = device
                if progress and task is not None:
                    progress.update(task, advance=1)

        workers = max(1, min(len(targets), self.concurrency // max(1, len(self.services))))
        async with asyncio.TaskGroup() as tg:
            for _ in range(workers):
                tg.create_task(worker())

    async def _scan_target(
        self,
        ip: str,
        swept: set[str] | None,
        probes: asyncio.Semaphore,
        lookups: asyncio.Semaphore,
    ) -> Device:
        if swept is not None and ip not in swept:
            return Device(ip=ip, errors=[HOST_DOWN])
        return await self.scan_device(
            ip, probes=probes, known_up=swept is not None, lookups=lookups
        )
