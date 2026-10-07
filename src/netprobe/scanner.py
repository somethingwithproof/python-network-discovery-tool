"""Host discovery and port checks driven by nmap."""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import os
import re
import socket

import nmap
from rich.progress import Progress

from netprobe.models import Device

logger = logging.getLogger(__name__)

# Largest network accepted in one run. A /8 would otherwise queue 16M scan tasks.
MAX_HOSTS = 65536
# Per-nmap-invocation cap so one unresponsive host cannot hang a scan.
NMAP_HOST_TIMEOUT = "30s"

_HOSTNAME_LABEL = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")


def _host_key(nm: nmap.PortScanner, target: str) -> str | None:
    """Find the result entry for target; nmap keys results by IP, not hostname."""
    hosts = nm.all_hosts()
    if target in hosts:
        return target
    try:
        ipaddress.ip_address(target)
    except ValueError:
        return hosts[0] if len(hosts) == 1 else None
    return None


def validate_target(target: str) -> str:
    """Return target if it is an IP address or a DNS name, else raise ValueError.

    The value is later passed to the nmap command line, so anything that could
    be read as an option (leading "-") or contains whitespace is rejected.
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


class NetworkScanner:
    """Fast async network scanner using nmap."""

    def __init__(self) -> None:
        # Constructed once up front so a missing nmap binary fails here.
        self.nm = self._new_scanner()

    def _new_scanner(self) -> nmap.PortScanner:
        """Return a fresh PortScanner.

        PortScanner keeps the last result on the instance, so sharing one
        across concurrent scans lets threads overwrite each other's output.
        """
        return nmap.PortScanner()

    async def scan_device(self, ip: str) -> Device:
        """Scan a single device for services.

        Args:
            ip: IP address or hostname to scan

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
            # Check if host is alive (faster than port scan)
            alive = await asyncio.to_thread(self._check_alive, ip)
            device.alive = alive

            if not alive:
                device.errors.append("Host is down")
                return device

            ports_to_check = {
                22: ("ssh", "tcp"),
                161: ("snmp", "udp"),
                3306: ("mysql", "tcp"),
            }

            if os.name == "posix" and os.geteuid() != 0:
                # nmap refuses UDP scans without raw-socket privileges.
                del ports_to_check[161]
                device.errors.append("SNMP check skipped: UDP scan requires root")

            results: dict[int, bool | Exception] = {}

            async def check(port: int, proto: str) -> None:
                try:
                    results[port] = await self._check_port(ip, port, proto)
                except Exception as e:
                    results[port] = e

            async with asyncio.TaskGroup() as tg:
                for port, (_, proto) in ports_to_check.items():
                    tg.create_task(check(port, proto))

            for port, (attr, _) in ports_to_check.items():
                result = results[port]
                if isinstance(result, Exception):
                    device.errors.append(f"Error checking port {port}: {result}")
                else:
                    setattr(device, attr, result)

            # Try to get hostname
            try:
                device.hostname = await asyncio.to_thread(self._get_hostname, ip)
            except Exception as e:
                logger.debug(f"Could not resolve hostname for {ip}: {e}")

        except Exception as e:
            device.errors.append(f"Scan error: {e}")
            logger.error(f"Error scanning {ip}: {e}")

        return device

    def _check_alive(self, ip: str) -> bool:
        """Check if host is alive using nmap ping scan."""
        try:
            nm = self._new_scanner()
            nm.scan(hosts=ip, arguments=f"-sn -T4 --host-timeout {NMAP_HOST_TIMEOUT}")
            key = _host_key(nm, ip)
            return key is not None and nm[key].state() == "up"
        except Exception as e:
            logger.warning(f"Alive check failed for {ip}: {e}")
            return False

    async def _check_port(self, ip: str, port: int, proto: str = "tcp") -> bool:
        """Check if a specific port is open."""
        try:
            nm = self._new_scanner()
            udp = "-sU " if proto == "udp" else ""
            await asyncio.to_thread(
                nm.scan,
                hosts=ip,
                arguments=f"{udp}-p {port} -T4 --open --host-timeout {NMAP_HOST_TIMEOUT}",
            )

            key = _host_key(nm, ip)
            if key is None:
                return False

            port_info = nm[key].get(proto, {}).get(port, {})
            return bool(port_info.get("state") == "open")

        except Exception as e:
            logger.debug(f"Error checking port {port} on {ip}: {e}")
            return False

    def _get_hostname(self, ip: str) -> str:
        """Get hostname for IP address."""
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return ""

    async def scan_network(self, network: str, progress: Progress | None = None) -> list[Device]:
        """Scan an entire network.

        Args:
            network: Network in CIDR notation (e.g., "192.168.1.0/24"), IP, or hostname
            progress: Optional Rich progress bar

        Returns:
            List of scanned devices

        Raises:
            ValueError: if the target is malformed or larger than MAX_HOSTS
        """
        try:
            if "/" in network:
                net = ipaddress.ip_network(network, strict=False)
                if net.num_addresses > MAX_HOSTS:
                    raise ValueError(
                        f"Network too large: {net.num_addresses} addresses (max {MAX_HOSTS})"
                    )
                ips = [str(ip) for ip in net.hosts()]
            else:
                ips = [validate_target(network)]
        except ValueError as e:
            raise ValueError(f"Invalid network format: {e}") from e

        logger.info(f"Scanning {len(ips)} hosts...")

        # Create progress task if progress bar provided
        task = progress.add_task("[cyan]Scanning network...", total=len(ips)) if progress else None

        # Limit concurrency: each device scan spawns several nmap processes
        semaphore = asyncio.Semaphore(20)

        async def scan_with_progress(ip: str) -> Device:
            async with semaphore:
                result = await self.scan_device(ip)
                if progress and task is not None:
                    progress.update(task, advance=1)
                return result

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(scan_with_progress(ip)) for ip in ips]

        return [t.result() for t in tasks]
