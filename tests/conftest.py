# SPDX-FileCopyrightText: 2025-2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Local socket fixtures. Every test server binds to 127.0.0.1 only."""

from __future__ import annotations

import asyncio
import contextlib
import json
import socket
from collections.abc import AsyncIterator, Callable
from importlib.resources import files
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

FIXTURES = Path(__file__).parent / "fixtures"

# The published JSON Schemas, keyed by file name, resolved through their $id.
SCHEMAS = {
    path.name: json.loads(path.read_text())
    for path in files("netprobe").joinpath("schemas").iterdir()
    if path.name.endswith(".schema.json")
}


def composed_targets(schemas):
    """(file, JSON pointer) of every subschema that is only used through allOf."""
    targets = set()
    for name, schema in schemas.items():
        for part in schema.get("allOf", []):
            ref = part.get("$ref", "")
            path, _, pointer = ref.partition("#")
            targets.add((path or name, pointer))
    return targets


def closed(node, name, pointer, skip):
    """Copy of a schema that rejects every property it does not declare.

    The published schemas accept unknown fields so that an additive change does
    not break consumers; the tests use closed copies so a field netprobe writes
    without documenting it fails here instead. unevaluatedProperties sees through
    allOf, so composed parts are left open and their composite is closed.
    Objects whose schema says additionalProperties: true stay open.
    """
    if isinstance(node, list):
        return [closed(item, name, f"{pointer}/{i}", skip) for i, item in enumerate(node)]
    if not isinstance(node, dict):
        return node
    copy = {key: closed(value, name, f"{pointer}/{key}", skip) for key, value in node.items()}
    if "properties" in copy and "additionalProperties" not in copy and (name, pointer) not in skip:
        copy["unevaluatedProperties"] = False
    return copy


def registry(schemas):
    return Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values()
    )


PUBLISHED = registry(SCHEMAS)
CLOSED_SCHEMAS = {
    name: closed(schema, name, "", composed_targets(SCHEMAS)) for name, schema in SCHEMAS.items()
}
CLOSED = registry(CLOSED_SCHEMAS)


def validator(name, *, published=False):
    """Closed validator by default; published=True uses the shipped schema."""
    schemas, store = (SCHEMAS, PUBLISHED) if published else (CLOSED_SCHEMAS, CLOSED)
    return Draft202012Validator(
        schemas[f"{name}-v1.schema.json"],
        registry=store,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )


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
