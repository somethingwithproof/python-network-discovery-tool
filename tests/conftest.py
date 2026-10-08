"""Local socket fixtures. Every test server binds to 127.0.0.1 only."""

from __future__ import annotations

import asyncio
import contextlib
import socket
from collections.abc import AsyncIterator, Callable
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def fixture_bytes(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


def closed_port(kind: int = socket.SOCK_STREAM) -> int:
    """Return a port that nothing listens on (bound, then released)."""
    with socket.socket(socket.AF_INET, kind) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture
async def tcp_server() -> AsyncIterator[Callable[[bytes], asyncio.Future[int]]]:
    """Start TCP servers that send a greeting on connect; yields a factory returning the port."""
    servers: list[asyncio.Server] = []

    async def start(greeting: bytes = b"") -> int:
        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            if greeting:
                writer.write(greeting)
                await writer.drain()
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(reader.read(4096), 2)
            writer.close()

        server = await asyncio.start_server(handle, "127.0.0.1", 0)
        servers.append(server)
        return int(server.sockets[0].getsockname()[1])

    def factory(greeting: bytes = b"") -> asyncio.Future[int]:
        return asyncio.ensure_future(start(greeting))

    yield factory
    for server in servers:
        server.close()
        await server.wait_closed()


class _Responder(asyncio.DatagramProtocol):
    def __init__(self, reply: bytes) -> None:
        self.reply = reply
        self.transport: asyncio.DatagramTransport | None = None
        self.received: list[bytes] = []

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        assert isinstance(transport, asyncio.DatagramTransport)
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str | int, ...]) -> None:
        self.received.append(data)
        if self.reply and self.transport:
            self.transport.sendto(self.reply, addr)


@pytest.fixture
async def udp_server() -> AsyncIterator[Callable[[bytes], asyncio.Future[tuple[int, _Responder]]]]:
    """Start UDP responders that answer every datagram with fixed bytes."""
    transports: list[asyncio.BaseTransport] = []

    async def start(reply: bytes) -> tuple[int, _Responder]:
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: _Responder(reply), local_addr=("127.0.0.1", 0)
        )
        transports.append(transport)
        return int(transport.get_extra_info("sockname")[1]), protocol

    def factory(reply: bytes = b"") -> asyncio.Future[tuple[int, _Responder]]:
        return asyncio.ensure_future(start(reply))

    yield factory
    for transport in transports:
        transport.close()
