"""Record raw protocol bytes from the integration lab for parser tests.

Run inside the lab network, e.g.:
    docker compose -f tests/integration/compose.yml run --rm tester \
        python tests/fixtures/capture.py tests/fixtures
"""

from __future__ import annotations

import socket
import ssl
import sys
from pathlib import Path

SSH = ("172.30.57.10", 22)
MARIADB = ("172.30.57.11", 3306)
SNMP = ("172.30.57.12", 161)
WEB = "172.30.57.13"

# SNMPv3 GetRequest with an empty engine ID and user, flags "reportable".
# RFC 3414 section 4 requires an agent to answer it with a Report carrying
# its engine ID, so it needs no credentials.
SNMPV3_DISCOVERY = bytes.fromhex(
    "303a020103300f02024a69020300ffe30401040201030410300e0400020100020100"
    "040004000400301204000400a00c020237f00201000201003000"
)


def first_read(addr: tuple[str, int], send: bytes = b"") -> bytes:
    with socket.create_connection(addr, timeout=5) as sock:
        if send:
            sock.sendall(send)
        return sock.recv(4096)


def snmp_report(addr: tuple[str, int]) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(SNMPV3_DISCOVERY, addr)
        return sock.recv(4096)


def http_response(host: str, port: int, tls: bool) -> bytes:
    raw = socket.create_connection((host, port), timeout=5)
    if tls:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        raw = ctx.wrap_socket(raw)
        (Path(sys.argv[1]) / "nginx-cert.der").write_bytes(raw.getpeercert(binary_form=True) or b"")
    with raw:
        raw.sendall(b"HEAD / HTTP/1.0\r\nHost: lab\r\n\r\n")
        return raw.recv(4096)


def main() -> None:
    out = Path(sys.argv[1])
    targets = sys.argv[2:] or ["ssh", "mariadb", "snmp", "web"]
    if "ssh" in targets:
        (out / "ssh-banner.bin").write_bytes(first_read(SSH))
    if "mariadb" in targets:
        (out / "mariadb-handshake.bin").write_bytes(first_read(MARIADB))
    if "snmp" in targets:
        (out / "snmpv3-report.bin").write_bytes(snmp_report(SNMP))
    if "web" in targets:
        (out / "nginx-http-head.bin").write_bytes(http_response(WEB, 80, tls=False))
        (out / "nginx-https-head.bin").write_bytes(http_response(WEB, 443, tls=True))


if __name__ == "__main__":
    main()
