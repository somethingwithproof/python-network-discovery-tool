# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Property tests for the untrusted input every scan starts from or reads back:
targets and CIDR ranges, and the BER in SNMPv3 replies."""

from __future__ import annotations

import ipaddress
import string

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from netprobe.probes import MAX_ENGINE_ID_OCTETS, snmp_engine_id
from netprobe.scanner import MAX_HOSTS, expand_targets, validate_target

LABEL = st.from_regex(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", fullmatch=True)
HOSTNAME = (
    st.lists(LABEL, min_size=1, max_size=4)
    .map(".".join)
    .filter(lambda name: len(name) <= 253 and not name.rsplit(".", 1)[-1].isdigit())
)
ADDRESS = st.one_of(st.ip_addresses(v=4), st.ip_addresses(v=6))
# Keep expansion small enough to enumerate quickly: at most 4096 addresses.
NETWORK = st.one_of(
    st.ip_addresses(v=4).flatmap(
        lambda ip: st.integers(20, 32).map(
            lambda prefix: ipaddress.ip_network(f"{ip}/{prefix}", strict=False)
        )
    ),
    st.ip_addresses(v=6).flatmap(
        lambda ip: st.integers(116, 128).map(
            lambda prefix: ipaddress.ip_network(f"{ip}/{prefix}", strict=False)
        )
    ),
)
# Characters that could split an argv entry or start an option on the nmap command line.
UNSAFE = st.sampled_from([" ", "\t", "\n", "\r", "\x00", "%", ";", "/", "\\", "'", '"'])


@given(ADDRESS)
def test_any_address_is_accepted_in_canonical_form(address):
    assert validate_target(str(address)) == str(address)
    if address.version == 6:
        assert validate_target(address.exploded) == str(address)


@given(HOSTNAME)
def test_well_formed_hostnames_are_returned_unchanged(name):
    assert validate_target(name) == name


@given(HOSTNAME, UNSAFE, st.integers(0, 300))
def test_hostnames_containing_unsafe_characters_are_rejected(name, char, position):
    position %= len(name) + 1
    with pytest.raises(ValueError):
        validate_target(name[:position] + char + name[position:])


@given(HOSTNAME)
def test_option_like_targets_are_rejected(name):
    with pytest.raises(ValueError):
        validate_target("-" + name)


@given(st.text(string.printable + "\x00é", max_size=300))
def test_accepted_targets_are_safe_nmap_arguments(text):
    try:
        target = validate_target(text)
    except ValueError:
        return
    assert not target.startswith("-")
    assert target.isprintable()
    assert not any(char.isspace() for char in target)
    assert "%" not in target


@given(NETWORK)
def test_expansion_lists_each_host_of_the_network_once_in_order(network):
    targets = expand_targets(str(network))
    addresses = [ipaddress.ip_address(target) for target in targets]
    assert addresses == sorted(set(addresses))
    assert addresses == list(network.hosts())
    assert all(address in network for address in addresses)


@given(NETWORK, st.integers(1, MAX_HOSTS))
def test_host_limit_is_checked_against_the_whole_network(network, limit):
    if network.num_addresses > limit:
        with pytest.raises(ValueError, match="too large"):
            expand_targets(str(network), max_hosts=limit)
    else:
        assert expand_targets(str(network), max_hosts=limit)


@given(NETWORK, st.data())
def test_exclusions_remove_exactly_the_excluded_hosts(network, data):
    hosts = list(network.hosts())
    excluded = data.draw(
        st.lists(st.sampled_from(hosts), max_size=8, unique=True), label="excluded"
    )
    remaining = [host for host in hosts if host not in excluded]
    exclusions = [str(host) for host in excluded]
    if not remaining:
        with pytest.raises(ValueError, match="No targets remain"):
            expand_targets(str(network), exclusions=exclusions)
        return
    targets = expand_targets(str(network), exclusions=exclusions)
    assert [ipaddress.ip_address(target) for target in targets] == remaining


@given(NETWORK, st.integers(0, 32))
def test_a_covering_exclusion_leaves_nothing_to_scan(network, widen):
    covering = network.supernet(prefixlen_diff=min(widen, network.prefixlen))
    with pytest.raises(ValueError, match="No targets remain"):
        expand_targets(str(network), exclusions=[str(covering)])


@given(st.text(max_size=100), st.lists(st.text(max_size=40), max_size=3))
def test_malformed_input_raises_only_value_error(network, exclusions):
    assume(network.strip())
    try:
        expand_targets(network, exclusions=exclusions)
    except ValueError as exc:
        assert str(exc).startswith("Invalid network format: ")


def ber(tag: int, value: bytes, long_form: bool = False) -> bytes:
    """Encode one BER TLV, optionally with a long-form length."""
    if long_form or len(value) > 0x7F:
        width = max(1, (len(value).bit_length() + 7) // 8)
        return bytes([tag, 0x80 | width]) + len(value).to_bytes(width, "big") + value
    return bytes([tag, len(value)]) + value


def snmpv3_report(engine_id: bytes, long_form: bool) -> bytes:
    usm = ber(0x30, ber(0x04, engine_id, long_form) + ber(0x02, b"\x00") + ber(0x02, b"\x00"))
    body = (
        ber(0x02, b"\x03")
        + ber(0x30, ber(0x02, b"\x01") + ber(0x02, b"\x05\xdc") + ber(0x04, b"\x00"))
        + ber(0x04, usm, long_form)
        + ber(0x30, b"")
    )
    return ber(0x30, body, long_form)


@given(st.binary(min_size=1, max_size=300), st.booleans())
def test_engine_id_round_trips_through_ber(engine_id, long_form):
    message = snmpv3_report(engine_id, long_form)
    assert snmp_engine_id(message) == engine_id[:MAX_ENGINE_ID_OCTETS].hex()


@given(st.binary(min_size=1, max_size=64), st.booleans(), st.data())
def test_truncated_replies_yield_no_engine_id(engine_id, long_form, data):
    message = snmpv3_report(engine_id, long_form)
    cut = data.draw(st.integers(0, len(message) - 1), label="cut")
    assert snmp_engine_id(message[:cut]) is None


@given(st.binary(max_size=512))
def test_arbitrary_replies_never_raise(reply):
    engine_id = snmp_engine_id(reply)
    if engine_id is not None:
        assert 0 < len(engine_id) <= 2 * MAX_ENGINE_ID_OCTETS
        int(engine_id, 16)
