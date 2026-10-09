# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Service probes: reachability plus a read-only fingerprint of what answers.

Every probe stops at what a server volunteers before authentication: the SSH
identification string, the MySQL initial handshake, HTTP response headers,
the TLS certificate, and SNMP system MIB values when credentials are given.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import ssl
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from cryptography import x509

from netprobe.models import Protocol

logger = logging.getLogger(__name__)

PortState = Literal["open", "closed", "filtered"]
Details = dict[str, Any]

# Banners are attacker-controlled; keep stored strings short and printable.
MAX_TEXT = 256
MAX_HEADER_BYTES = 16384
# StreamReader line limit; an SSH identification line is at most 255 bytes.
MAX_LINE_BYTES = 4096
# A real MySQL greeting is under 200 bytes; refuse to buffer a 16 MB "packet".
MAX_MYSQL_PACKET = 4096

# SNMPv3 GetRequest with an empty engine ID and user and the reportable flag.
# RFC 3414 section 4 requires an agent to answer it with a Report carrying its
# engine ID, so the probe needs no community string or credentials.
SNMPV3_DISCOVERY = bytes.fromhex(
    "303a020103300f02024a69020300ffe30401040201030410300e0400020100020100"
    "040004000400301204000400a00c020237f00201000201003000"
)

SYSTEM_OIDS = {
    "sys_descr": "1.3.6.1.2.1.1.1.0",
    "sys_object_id": "1.3.6.1.2.1.1.2.0",
    "sys_name": "1.3.6.1.2.1.1.5.0",
}

# Names match the auth and privacy protocol lists Cacti and Kadupul accept.
AUTH_PROTOCOLS = ("MD5", "SHA", "SHA224", "SHA256", "SHA384", "SHA512")
PRIV_PROTOCOLS = ("DES", "AES", "AES128", "AES192", "AES192C", "AES256", "AES256C")


@dataclass(frozen=True)
class SnmpCredentials:
    """SNMP access for the system MIB query. Secrets are kept out of repr()."""

    community: str | None = field(default=None, repr=False)
    user: str | None = None
    auth_protocol: str = "SHA"
    auth_key: str | None = field(default=None, repr=False)
    priv_protocol: str = "AES"
    priv_key: str | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        # Refuse ambiguous or weakened settings rather than quietly picking a
        # lower security level than the caller asked for.
        if self.community and self.user:
            raise ValueError("give either an SNMP community (v2c) or an SNMPv3 user, not both")
        if self.priv_key and not self.auth_key:
            raise ValueError("an SNMPv3 privacy key needs an authentication key as well")
        if (self.auth_key or self.priv_key) and not self.user:
            raise ValueError("SNMPv3 keys need an SNMPv3 user")
        if self.auth_protocol not in AUTH_PROTOCOLS:
            raise ValueError(f"unknown SNMPv3 auth protocol {self.auth_protocol!r}")
        if self.priv_protocol not in PRIV_PROTOCOLS:
            raise ValueError(f"unknown SNMPv3 privacy protocol {self.priv_protocol!r}")

    @property
    def version(self) -> str:
        return "3" if self.user else "2c"

    @property
    def security_level(self) -> str:
        if not self.user:
            return ""
        if self.priv_key:
            return "authPriv"
        return "authNoPriv" if self.auth_key else "noAuthNoPriv"

    def redact(self, text: str) -> str:
        """Remove any secret that might have been echoed into text."""
        for secret in (self.community, self.auth_key, self.priv_key):
            if secret:
                text = text.replace(secret, "***")
        return text


@dataclass(frozen=True)
class ProbeContext:
    timeout: float
    snmp: SnmpCredentials | None = None
    tls_ca_file: str | None = None


@dataclass
class ProbeResult:
    state: PortState
    version: str = ""
    details: Details = field(default_factory=dict)


def clean(raw: bytes | str, limit: int = MAX_TEXT) -> str:
    """Decode untrusted bytes into a short single-line printable string."""
    text = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else raw
    return "".join(c if c.isprintable() else " " for c in text).strip()[:limit]


# --- TCP -------------------------------------------------------------------


async def _open(
    host: str, port: int, timeout_seconds: float, tls: ssl.SSLContext | None = None
) -> tuple[asyncio.StreamReader, asyncio.StreamWriter] | PortState:
    """Connect, returning the streams, or the port state when the connect fails.

    TLS errors propagate so the HTTPS probe can tell them apart.
    """
    try:
        async with asyncio.timeout(timeout_seconds):
            return await asyncio.open_connection(
                host, port, ssl=tls, server_hostname=host if tls else None, limit=MAX_LINE_BYTES
            )
    except ConnectionRefusedError:
        return "closed"
    except ssl.SSLError:
        raise
    except OSError:
        return "filtered"


async def _close(writer: asyncio.StreamWriter) -> None:
    writer.close()
    with contextlib.suppress(OSError):
        async with asyncio.timeout(1):
            await writer.wait_closed()


async def tcp_state(host: str, port: int, timeout_seconds: float) -> PortState:
    """Classify a TCP port by attempting a full connect.

    A refused connection still proves the host is up, which is why "closed"
    is kept apart from "filtered" (no answer before the timeout).
    """
    streams = await _open(host, port, timeout_seconds)
    if isinstance(streams, str):
        return streams
    await _close(streams[1])
    return "open"


async def connect_probe(host: str, port: int, ctx: ProbeContext) -> ProbeResult:
    return ProbeResult(await tcp_state(host, port, ctx.timeout))


def parse_ssh_banner(line: bytes) -> Details:
    """Split an RFC 4253 identification string, SSH-proto-software [comments]."""
    text = clean(line)
    if not text.startswith("SSH-"):
        return {}
    ident, _, comments = text.partition(" ")
    _, proto, software = [*ident.split("-", 2), "", ""][:3]
    return {"protocol": proto, "software": software, "comments": comments}


async def ssh_probe(host: str, port: int, ctx: ProbeContext) -> ProbeResult:
    streams = await _open(host, port, ctx.timeout)
    if isinstance(streams, str):
        return ProbeResult(streams)
    reader, writer = streams
    details: Details = {}
    try:
        async with asyncio.timeout(ctx.timeout):
            # RFC 4253 lets a server send other lines before its identification.
            for _ in range(5):
                details = parse_ssh_banner(await reader.readline())
                if details:
                    break
    except (OSError, ValueError) as e:
        details = {"error": f"no banner: {clean(str(e)) or type(e).__name__}"}
    finally:
        await _close(writer)
    return ProbeResult("open", details.get("software", ""), details)


def parse_mysql_handshake(packet: bytes) -> Details:
    """Read the server greeting that MySQL and MariaDB send before any login.

    packet includes the 4-byte header (3-byte length, sequence number).
    """
    payload = packet[4 : 4 + int.from_bytes(packet[:3], "little")]
    if not payload:
        return {}
    if payload[0] == 0xFF:
        # Error packet, e.g. "Host ... is not allowed to connect to this server".
        message = payload[3:]
        if message.startswith(b"#"):
            message = message[6:]
        return {"error_code": int.from_bytes(payload[1:3], "little"), "error": clean(message)}
    if payload[0] != 10:
        return {}
    version, _, rest = payload[1:].partition(b"\0")
    server_version = clean(version)
    # MariaDB before 11 prefixes "5.5.5-" so old replicas accept it.
    if server_version.startswith("5.5.5-") and "MariaDB" in server_version:
        server_version = server_version[6:]
    details: Details = {
        "protocol": 10,
        "server_version": server_version,
        "flavor": "MariaDB" if "MariaDB" in server_version else "MySQL",
    }
    # connection id (4), auth data 1 (8), filler (1), capabilities low (2),
    # charset (1), status (2), capabilities high (2), auth data length (1),
    # reserved (10), auth data 2 (max(13, length - 8)), auth plugin name.
    if len(rest) >= 31:
        auth_len = rest[20]
        start = 31 + max(13, auth_len - 8)
        plugin, _, _ = rest[start:].partition(b"\0")
        if plugin:
            details["auth_plugin"] = clean(plugin)
    return details


async def mysql_probe(host: str, port: int, ctx: ProbeContext) -> ProbeResult:
    streams = await _open(host, port, ctx.timeout)
    if isinstance(streams, str):
        return ProbeResult(streams)
    reader, writer = streams
    try:
        async with asyncio.timeout(ctx.timeout):
            header = await reader.readexactly(4)
            length = int.from_bytes(header[:3], "little")
            if length > MAX_MYSQL_PACKET:
                raise ValueError(f"greeting of {length} bytes is too large")
            body = await reader.readexactly(length)
        details = parse_mysql_handshake(header + body)
    except (OSError, ValueError, asyncio.IncompleteReadError) as e:
        details = {"error": f"no handshake: {clean(str(e)) or type(e).__name__}"}
    finally:
        await _close(writer)
    return ProbeResult("open", details.get("server_version", ""), details)


def parse_http_head(raw: bytes) -> Details:
    """Pull the status code and Server header out of an HTTP response head."""
    head = raw.split(b"\r\n\r\n", 1)[0].split(b"\r\n")
    status_line = head[0].split(b" ", 2)
    if len(status_line) < 2 or not status_line[0].startswith(b"HTTP/"):
        return {}
    details: Details = {}
    if status_line[1].isdigit():
        details["status"] = int(status_line[1])
    for line in head[1:]:
        name, sep, value = line.partition(b":")
        if sep and name.strip().lower() == b"server":
            details["server"] = clean(value)
    return details


async def _http_exchange(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, host: str, timeout_seconds: float
) -> Details:
    writer.write(
        b"HEAD / HTTP/1.0\r\nHost: "
        + host.encode("idna")
        + b"\r\nUser-Agent: netprobe\r\nConnection: close\r\n\r\n"
    )
    try:
        async with asyncio.timeout(timeout_seconds):
            await writer.drain()
            raw = await reader.read(MAX_HEADER_BYTES)
    except OSError as e:
        return {"error": f"no response: {clean(str(e)) or type(e).__name__}"}
    if not raw:
        return {"error": "no response: connection closed"}
    return parse_http_head(raw) or {"error": "not an HTTP response"}


async def http_probe(host: str, port: int, ctx: ProbeContext) -> ProbeResult:
    streams = await _open(host, port, ctx.timeout)
    if isinstance(streams, str):
        return ProbeResult(streams)
    reader, writer = streams
    try:
        details = await _http_exchange(reader, writer, host, ctx.timeout)
    finally:
        await _close(writer)
    return ProbeResult("open", details.get("server", ""), details)


def parse_certificate(der: bytes) -> Details:
    """Summarise a DER certificate: subject, issuer, SANs and validity in UTC."""
    cert = x509.load_der_x509_certificate(der)
    sans: list[str] = []
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        sans += [f"DNS:{clean(n)}" for n in ext.get_values_for_type(x509.DNSName)]
        sans += [f"IP:{ip}" for ip in ext.get_values_for_type(x509.IPAddress)]
    except x509.ExtensionNotFound:
        pass
    subject = clean(cert.subject.rfc4514_string())
    issuer = clean(cert.issuer.rfc4514_string())
    return {
        "cert_subject": subject,
        "cert_issuer": issuer,
        "cert_sans": sans,
        "cert_not_before": cert.not_valid_before_utc.isoformat(),
        "cert_not_after": cert.not_valid_after_utc.isoformat(),
        "cert_self_signed": subject == issuer,
    }


def _tls_context(ca_file: str | None) -> ssl.SSLContext:
    """Authenticate TLS before collecting application or certificate observations."""
    return ssl.create_default_context(cafile=ca_file)


async def https_probe(host: str, port: int, ctx: ProbeContext) -> ProbeResult:
    verified_ctx = _tls_context(ctx.tls_ca_file)
    details: Details = {"cert_verified": True}
    try:
        streams = await _open(host, port, ctx.timeout, verified_ctx)
    except ssl.SSLCertVerificationError as e:
        return ProbeResult(
            "open",
            "",
            {
                "cert_verified": False,
                "cert_verify_error": clean(e.verify_message or str(e)),
            },
        )
    except ssl.SSLError as e:
        # Something listens but does not complete a TLS handshake.
        return ProbeResult("open", "", {"tls_error": clean(str(e))})
    if isinstance(streams, str):
        return ProbeResult(streams)

    reader, writer = streams
    try:
        tls = writer.get_extra_info("ssl_object")
        if isinstance(tls, ssl.SSLObject):
            details["tls_version"] = tls.version() or ""
            der = tls.getpeercert(binary_form=True)
            if der:
                try:
                    details.update(parse_certificate(der))
                except ValueError as e:
                    details["cert_error"] = clean(str(e))
        details.update(await _http_exchange(reader, writer, host, ctx.timeout))
    finally:
        await _close(writer)
    return ProbeResult("open", details.get("server", ""), details)


# --- SNMP ------------------------------------------------------------------


class _OneDatagram(asyncio.DatagramProtocol):
    def __init__(self) -> None:
        self.reply: asyncio.Future[bytes] = asyncio.get_running_loop().create_future()

    def datagram_received(self, data: bytes, addr: tuple[str | int, ...]) -> None:
        if not self.reply.done():
            self.reply.set_result(data)

    def error_received(self, exc: Exception) -> None:
        # Linux surfaces an ICMP port-unreachable as ECONNREFUSED here.
        if not self.reply.done():
            self.reply.set_exception(exc)


async def udp_exchange(
    host: str, port: int, payload: bytes, timeout_seconds: float
) -> bytes | None:
    """Send one datagram and return the first reply.

    Raises ConnectionRefusedError when the host answers with ICMP
    port-unreachable; returns None when nothing comes back in time.
    """
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        _OneDatagram, remote_addr=(host, port)
    )
    try:
        transport.sendto(payload)
        async with asyncio.timeout(timeout_seconds):
            return await protocol.reply
    except TimeoutError:
        return None
    finally:
        transport.close()


def _tlv(data: bytes, offset: int) -> tuple[int, bytes, int]:
    """Decode one BER tag-length-value at offset; return (tag, value, next offset)."""
    tag = data[offset]
    length = data[offset + 1]
    offset += 2
    if length & 0x80:
        width = length & 0x7F
        if width == 0 or width > 4:
            raise ValueError("unsupported BER length")
        length = int.from_bytes(data[offset : offset + width], "big")
        offset += width
    end = offset + length
    if end > len(data):
        raise ValueError("truncated BER value")
    return tag, data[offset:end], end


def snmp_engine_id(message: bytes) -> str | None:
    """Return the authoritative engine ID (hex) from an SNMPv3 message, else None."""
    try:
        tag, body, _ = _tlv(message, 0)
        if tag != 0x30:
            return None
        tag, version, pos = _tlv(body, 0)
        if tag != 0x02 or int.from_bytes(version, "big") != 3:
            return None
        _, _, pos = _tlv(body, pos)  # msgGlobalData
        tag, security, _ = _tlv(body, pos)
        if tag != 0x04:
            return None
        tag, usm, _ = _tlv(security, 0)
        if tag != 0x30:
            return None
        tag, engine_id, _ = _tlv(usm, 0)
    except (IndexError, ValueError):
        return None
    if tag != 0x04 or not engine_id:
        return None
    return engine_id.hex()


async def snmp_discover(
    host: str, port: int, timeout_seconds: float
) -> tuple[PortState, str | None]:
    """Send an unauthenticated SNMPv3 discovery request; return state and engine ID."""
    try:
        reply = await udp_exchange(host, port, SNMPV3_DISCOVERY, timeout_seconds)
    except ConnectionRefusedError:
        return "closed", None
    except OSError as e:
        logger.debug(f"SNMP probe of {host}:{port} failed: {e}")
        return "filtered", None
    engine_id = snmp_engine_id(reply) if reply else None
    return ("open" if engine_id else "filtered"), engine_id


async def snmp_system(
    host: str, port: int, creds: SnmpCredentials, timeout_seconds: float
) -> dict[str, str]:
    """GET sysDescr, sysObjectID and sysName. Raises RuntimeError on any SNMP error."""
    # Imported here: pysnmp loads its MIB machinery on import, which slows
    # every CLI start even when no credentials are given.
    from pysnmp.hlapi.v3arch import asyncio as hlapi

    auth: Any
    if creds.user:
        auth_map = {
            "MD5": hlapi.USM_AUTH_HMAC96_MD5,
            "SHA": hlapi.USM_AUTH_HMAC96_SHA,
            "SHA224": hlapi.USM_AUTH_HMAC128_SHA224,
            "SHA256": hlapi.USM_AUTH_HMAC192_SHA256,
            "SHA384": hlapi.USM_AUTH_HMAC256_SHA384,
            "SHA512": hlapi.USM_AUTH_HMAC384_SHA512,
        }
        # AES192/AES256 follow net-snmp's key extension; the C variants are Cisco's.
        priv_map = {
            "DES": hlapi.USM_PRIV_CBC56_DES,
            "AES": hlapi.USM_PRIV_CFB128_AES,
            "AES128": hlapi.USM_PRIV_CFB128_AES,
            "AES192": hlapi.USM_PRIV_CFB192_AES_BLUMENTHAL,
            "AES256": hlapi.USM_PRIV_CFB256_AES_BLUMENTHAL,
            "AES192C": hlapi.USM_PRIV_CFB192_AES,
            "AES256C": hlapi.USM_PRIV_CFB256_AES,
        }
        # SnmpCredentials already refused a privacy key without an auth key,
        # so the level used here is exactly the one the caller configured.
        auth = hlapi.UsmUserData(
            creds.user,
            authKey=creds.auth_key,
            privKey=creds.priv_key,
            authProtocol=auth_map[creds.auth_protocol] if creds.auth_key else hlapi.USM_AUTH_NONE,
            privProtocol=priv_map[creds.priv_protocol] if creds.priv_key else hlapi.USM_PRIV_NONE,
        )
    else:
        auth = hlapi.CommunityData(creds.community or "", mpModel=1)

    engine = hlapi.SnmpEngine()
    try:
        target = await hlapi.UdpTransportTarget.create(
            (host, port), timeout=timeout_seconds, retries=0
        )
        error, status, _, binds = await hlapi.get_cmd(
            engine,
            auth,
            target,
            hlapi.ContextData(),
            *[hlapi.ObjectType(hlapi.ObjectIdentity(oid)) for oid in SYSTEM_OIDS.values()],
        )
    finally:
        engine.close_dispatcher()
    if error:
        raise RuntimeError(creds.redact(clean(str(error))))
    if status:
        raise RuntimeError(creds.redact(clean(status.prettyPrint())))
    values = {str(oid): clean(str(value)) for oid, value in binds}
    return {name: values.get(oid, "") for name, oid in SYSTEM_OIDS.items()}


async def snmp_probe(host: str, port: int, ctx: ProbeContext) -> ProbeResult:
    state, engine_id = await snmp_discover(host, port, ctx.timeout)
    details: Details = {"engine_id": engine_id} if engine_id else {}
    creds = ctx.snmp
    if creds is None or not (creds.user or creds.community):
        return ProbeResult(state, "", details)
    try:
        system = await snmp_system(host, port, creds, ctx.timeout)
    except Exception as e:
        # A failed GET keeps whatever state discovery found and is never
        # retried with another SNMP version or a lower security level.
        details["snmp_error"] = creds.redact(clean(str(e))) or type(e).__name__
        return ProbeResult(state, "", details)
    details.update(system)
    details["snmp_version"] = creds.version
    if creds.security_level:
        details["snmp_security_level"] = creds.security_level
    return ProbeResult("open", system["sys_descr"], details)


Probe = Callable[[str, int, ProbeContext], Awaitable[ProbeResult]]

# Every probe a service can name in the config, and the transport it uses.
# Adding a service type means adding a function and a row here.
PROBES: dict[str, tuple[Probe, Protocol]] = {
    "tcp": (connect_probe, "tcp"),
    "ssh": (ssh_probe, "tcp"),
    "mysql": (mysql_probe, "tcp"),
    "http": (http_probe, "tcp"),
    "https": (https_probe, "tcp"),
    "snmp": (snmp_probe, "udp"),
}
