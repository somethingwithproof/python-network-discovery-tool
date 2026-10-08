"""Low-level reachability probes over asyncio sockets."""

from __future__ import annotations

import asyncio
import contextlib
import logging
from typing import Literal

logger = logging.getLogger(__name__)

PortState = Literal["open", "closed", "filtered"]

# SNMPv3 GetRequest with an empty engine ID and user and the reportable flag.
# RFC 3414 section 4 requires an agent to answer it with a Report carrying its
# engine ID, so the probe needs no community string or credentials.
SNMPV3_DISCOVERY = bytes.fromhex(
    "303a020103300f02024a69020300ffe30401040201030410300e0400020100020100"
    "040004000400301204000400a00c020237f00201000201003000"
)


async def tcp_state(host: str, port: int, timeout: float) -> PortState:
    """Classify a TCP port by attempting a full connect.

    A refused connection still proves the host is up, which is why "closed"
    is kept apart from "filtered" (no answer before the timeout).
    """
    try:
        async with asyncio.timeout(timeout):
            _, writer = await asyncio.open_connection(host, port)
    except ConnectionRefusedError:
        return "closed"
    except (TimeoutError, OSError):
        return "filtered"
    writer.close()
    with contextlib.suppress(OSError):
        await writer.wait_closed()
    return "open"


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


async def udp_exchange(host: str, port: int, payload: bytes, timeout: float) -> bytes | None:
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
        async with asyncio.timeout(timeout):
            return await protocol.reply
    except TimeoutError:
        return None
    finally:
        transport.close()


async def snmp_state(host: str, port: int, timeout: float) -> PortState:
    """Classify an SNMP agent with an unauthenticated SNMPv3 discovery request."""
    try:
        reply = await udp_exchange(host, port, SNMPV3_DISCOVERY, timeout)
    except ConnectionRefusedError:
        return "closed"
    except OSError as e:
        logger.debug(f"SNMP probe of {host}:{port} failed: {e}")
        return "filtered"
    if reply is None:
        return "filtered"
    return "open" if snmp_engine_id(reply) is not None else "filtered"


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
