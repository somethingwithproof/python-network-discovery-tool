import asyncio
import socket

import pytest
from conftest import closed_port, fixture_bytes

from netprobe import probes


async def test_tcp_state_open(tcp_server):
    port = await tcp_server(b"hello")
    assert await probes.tcp_state("127.0.0.1", port, 1.0) == "open"


async def test_tcp_state_closed():
    assert await probes.tcp_state("127.0.0.1", closed_port(), 1.0) == "closed"


async def test_tcp_state_filtered_on_timeout(monkeypatch):
    async def never_connects(host, port, **kwargs):
        await asyncio.sleep(10)

    monkeypatch.setattr(asyncio, "open_connection", never_connects)
    assert await probes.tcp_state("127.0.0.1", 1, 0.05) == "filtered"


async def test_tcp_state_filtered_on_unreachable(monkeypatch):
    async def unreachable(host, port, **kwargs):
        raise OSError(113, "No route to host")

    monkeypatch.setattr(asyncio, "open_connection", unreachable)
    assert await probes.tcp_state("127.0.0.1", 1, 1.0) == "filtered"


async def test_udp_exchange_returns_reply_and_sends_payload(udp_server):
    port, responder = await udp_server(b"pong")

    assert await probes.udp_exchange("127.0.0.1", port, b"ping", 1.0) == b"pong"
    assert responder.received == [b"ping"]


async def test_udp_exchange_times_out(udp_server):
    port, _ = await udp_server(b"")
    assert await probes.udp_exchange("127.0.0.1", port, b"ping", 0.05) is None


ENGINE_ID = "80001f88808aa1f93d7edcc66a00000000"


async def test_snmp_discover_open_on_real_report(udp_server):
    port, responder = await udp_server(fixture_bytes("snmpv3-report.bin"))

    assert await probes.snmp_discover("127.0.0.1", port, 1.0) == ("open", ENGINE_ID)
    assert responder.received == [probes.SNMPV3_DISCOVERY]


async def test_snmp_discover_filtered_on_garbage_or_silence(udp_server):
    garbage, _ = await udp_server(b"not snmp")
    silent, _ = await udp_server(b"")

    assert await probes.snmp_discover("127.0.0.1", garbage, 0.2) == ("filtered", None)
    assert await probes.snmp_discover("127.0.0.1", silent, 0.05) == ("filtered", None)


async def test_snmp_discover_closed_on_icmp_unreachable(monkeypatch):
    async def refused(*args):
        raise ConnectionRefusedError

    monkeypatch.setattr(probes, "udp_exchange", refused)
    assert await probes.snmp_discover("127.0.0.1", 161, 1.0) == ("closed", None)


async def test_snmp_discover_filtered_on_socket_error(monkeypatch):
    async def broken(*args):
        raise OSError("network unreachable")

    monkeypatch.setattr(probes, "udp_exchange", broken)
    assert await probes.snmp_discover("127.0.0.1", 161, 1.0) == ("filtered", None)


async def test_snmp_discover_against_closed_udp_port():
    # Loopback answers with ICMP port-unreachable on Linux (closed); macOS stays silent.
    state, _ = await probes.snmp_discover("127.0.0.1", closed_port(socket.SOCK_DGRAM), 0.2)
    assert state in {"closed", "filtered"}


def test_snmp_engine_id_from_captured_net_snmp_report():
    # Captured from net-snmp 5.9 in the integration lab (tests/fixtures/capture.py).
    assert probes.snmp_engine_id(fixture_bytes("snmpv3-report.bin")) == ENGINE_ID


def test_snmp_engine_id_of_our_own_request_is_empty():
    assert probes.snmp_engine_id(probes.SNMPV3_DISCOVERY) is None


@pytest.mark.parametrize(
    "message",
    [
        b"",
        b"\x30",
        b"\x02\x01\x03",
        bytes.fromhex("3003020101"),  # SNMPv2c message
        bytes.fromhex("30050201030400"),  # globalData is not where expected
        bytes.fromhex("3084ffffffff"),  # long-form length past the end
        bytes.fromhex("3080"),  # indefinite length is not allowed in SNMP
        bytes.fromhex("30080201033000020105"),  # security params are not an octet string
        bytes.fromhex("300b0201033000040430020400"),  # USM sequence with empty engine ID
        bytes.fromhex("300a02010330000403020100"),  # USM is not a sequence
    ],
)
def test_snmp_engine_id_rejects_malformed(message):
    assert probes.snmp_engine_id(message) is None
