# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

import pytest

from netprobe.config import DEFAULT_SERVICES, ConfigError, load_services, select_services
from netprobe.probes import PROBES


def test_defaults_cover_the_documented_services():
    assert [(s.name, s.port, s.protocol, s.probe) for s in DEFAULT_SERVICES] == [
        ("ssh", 22, "tcp", "ssh"),
        ("snmp", 161, "udp", "snmp"),
        ("mysql", 3306, "tcp", "mysql"),
        ("http", 80, "tcp", "http"),
        ("https", 443, "tcp", "https"),
    ]
    assert all(s.probe in PROBES for s in DEFAULT_SERVICES)


def write(tmp_path, text):
    path = tmp_path / "netprobe.toml"
    path.write_text(text)
    return path


def test_config_adds_and_overrides(tmp_path):
    path = write(
        tmp_path,
        """
        [services.ssh]
        port = 2222

        [services.admin-ui]
        port = 8443
        probe = "https"

        [services.snmp-alt]
        port = 1161
        probe = "snmp"
        """,
    )
    services = {s.name: s for s in load_services(path)}

    assert services["ssh"].port == 2222
    assert services["ssh"].probe == "ssh"
    assert (services["admin-ui"].port, services["admin-ui"].probe) == (8443, "https")
    assert services["snmp-alt"].protocol == "udp"
    assert services["mysql"].port == 3306


def test_config_without_services_table_keeps_defaults(tmp_path):
    assert load_services(write(tmp_path, "")) == DEFAULT_SERVICES


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("services = 1", "must be a table"),
        ("[services]\nweb = 80", "must be a table"),
        ("[services.web]\nport = 0", "port must be"),
        ("[services.web]\nport = true", "port must be"),
        ("[services.web]\nprobe = 'http'", "port must be"),
        ("[services.web]\nport = 80\nprobe = 'gopher'", "unknown probe"),
        ("[services.web]\nport = 80\nhost = 'x'", "unknown keys"),
        ('[services."Bad Name"]\nport = 80', "invalid service name"),
        ("[services.web\nport = 80", "cannot read config"),
    ],
)
def test_config_errors(tmp_path, text, message):
    prepared_argument_0 = write(tmp_path, text)
    with pytest.raises(ConfigError, match=message):
        load_services(prepared_argument_0)


def test_missing_config_file(tmp_path):
    with pytest.raises(ConfigError, match="cannot read config"):
        load_services(tmp_path / "absent.toml")


def test_select_by_name_keeps_requested_order():
    selected = select_services(DEFAULT_SERVICES, "https, ssh", None)
    assert [s.name for s in selected] == ["https", "ssh"]


def test_ports_override_and_add():
    selected = select_services(DEFAULT_SERVICES, "ssh", "ssh=2222, 9000,")
    assert [(s.name, s.port, s.protocol, s.probe) for s in selected] == [
        ("ssh", 2222, "tcp", "ssh"),
        ("tcp-9000", 9000, "tcp", "tcp"),
    ]


def test_no_selection_returns_everything():
    assert select_services(DEFAULT_SERVICES, None, None) == DEFAULT_SERVICES


@pytest.mark.parametrize(
    ("names", "ports", "message"),
    [
        ("telnet", None, "unknown service"),
        (None, "abc", "expected PORT"),
        (None, "ssh=", "expected PORT"),
        (None, "70000", "port must be"),
        (None, "telnet=23", "unknown service"),
        (",", None, "no services selected"),
    ],
)
def test_selection_errors(names, ports, message):
    with pytest.raises(ConfigError, match=message):
        select_services(DEFAULT_SERVICES, names, ports)


def test_too_many_services_from_ports():
    ports = ",".join(str(p) for p in range(1000, 1070))
    with pytest.raises(ConfigError, match="max 64"):
        select_services(DEFAULT_SERVICES, None, ports)


def test_too_many_services_from_config(tmp_path):
    text = "".join(f"[services.s{i}]\nport = {1000 + i}\n" for i in range(70))
    prepared_argument_0 = write(tmp_path, text)
    with pytest.raises(ConfigError, match="max 64"):
        load_services(prepared_argument_0)
