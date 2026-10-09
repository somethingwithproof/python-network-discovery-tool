"""Fingerprint parsers and probes, driven by bytes captured from the lab."""

import asyncio
import datetime as dt
import ipaddress
import ssl

import pytest
from conftest import closed_port, fixture_bytes
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID

from netprobe import probes
from netprobe.probes import ProbeContext, SnmpCredentials

CTX = ProbeContext(timeout=1.0)


# --- SSH


def test_parse_real_openssh_banner():
    assert probes.parse_ssh_banner(fixture_bytes("ssh-banner.bin")) == {
        "protocol": "2.0",
        "software": "OpenSSH_10.0",
        "comments": "",
    }


def test_parse_banner_with_comments_and_junk():
    assert probes.parse_ssh_banner(b"SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13\r\n") == {
        "protocol": "2.0",
        "software": "OpenSSH_9.6p1",
        "comments": "Ubuntu-3ubuntu13",
    }
    assert probes.parse_ssh_banner(b"SSH-1.99\r\n")["software"] == ""
    assert probes.parse_ssh_banner(b"220 smtp ready\r\n") == {}


def test_clean_strips_control_characters_and_truncates():
    assert probes.clean(b"a\x1b[31mb\x00c\r\n") == "a [31mb c"
    assert len(probes.clean("x" * 1000)) == probes.MAX_TEXT


async def test_ssh_probe_reads_banner_after_preamble(tcp_server):
    port = await tcp_server(b"welcome to the lab\r\n" + fixture_bytes("ssh-banner.bin"))
    result = await probes.ssh_probe("127.0.0.1", port, CTX)

    assert (result.state, result.version) == ("open", "OpenSSH_10.0")


async def test_ssh_probe_silent_server(tcp_server):
    port = await tcp_server(b"")
    result = await probes.ssh_probe("127.0.0.1", port, ProbeContext(timeout=0.2))

    assert result.state == "open"
    assert result.version == ""
    assert result.details["error"].startswith("no banner")


async def test_ssh_probe_closed_port():
    assert (await probes.ssh_probe("127.0.0.1", closed_port(), CTX)).state == "closed"


# --- MySQL / MariaDB


def test_parse_real_mariadb_handshake():
    assert probes.parse_mysql_handshake(fixture_bytes("mariadb-handshake.bin")) == {
        "protocol": 10,
        "server_version": "11.4.13-MariaDB-ubu2404",
        "flavor": "MariaDB",
        "auth_plugin": "mysql_native_password",
    }


def test_parse_real_mysql84_handshake():
    assert probes.parse_mysql_handshake(fixture_bytes("mysql84-handshake.bin")) == {
        "protocol": 10,
        "server_version": "8.4.11",
        "flavor": "MySQL",
        "auth_plugin": "caching_sha2_password",
    }


def packet(payload: bytes) -> bytes:
    return len(payload).to_bytes(3, "little") + b"\0" + payload


def test_parse_mariadb_replication_prefix():
    details = probes.parse_mysql_handshake(packet(b"\n5.5.5-10.6.18-MariaDB\0"))
    assert details["server_version"] == "10.6.18-MariaDB"


def test_parse_mysql_error_packet():
    message = b"Host '10.0.0.9' is not allowed to connect to this MariaDB server"
    details = probes.parse_mysql_handshake(packet(b"\xff\x6a\x04" + message))
    assert details == {"error_code": 1130, "error": message.decode()}

    with_state = probes.parse_mysql_handshake(packet(b"\xff\x10\x04#08S01Too many connections"))
    assert with_state["error"] == "Too many connections"


@pytest.mark.parametrize("raw", [b"", packet(b""), packet(b"\x09old protocol\0")])
def test_parse_mysql_rejects_other_payloads(raw):
    assert probes.parse_mysql_handshake(raw) == {}


async def test_mysql_probe_reads_greeting(tcp_server):
    port = await tcp_server(fixture_bytes("mariadb-handshake.bin"))
    result = await probes.mysql_probe("127.0.0.1", port, CTX)

    assert (result.state, result.version) == ("open", "11.4.13-MariaDB-ubu2404")


async def test_mysql_probe_truncated_greeting(tcp_server):
    port = await tcp_server(fixture_bytes("mariadb-handshake.bin")[:10])
    result = await probes.mysql_probe("127.0.0.1", port, ProbeContext(timeout=0.2))

    assert result.state == "open"
    assert result.details["error"].startswith("no handshake")


async def test_mysql_probe_closed_port():
    assert (await probes.mysql_probe("127.0.0.1", closed_port(), CTX)).state == "closed"


# --- HTTP


def test_parse_real_nginx_head():
    assert probes.parse_http_head(fixture_bytes("nginx-http-head.bin")) == {
        "status": 200,
        "server": "nginx/1.28.3",
    }


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (b"HTTP/1.1 301 Moved\r\nserver:  Apache \r\n\r\n", {"status": 301, "server": "Apache"}),
        (b"HTTP/1.0 xyz\r\n\r\n", {}),
        (b"SSH-2.0-OpenSSH_10.0\r\n", {}),
        (b"", {}),
    ],
)
def test_parse_http_head_variants(raw, expected):
    assert probes.parse_http_head(raw) == expected


async def test_http_probe_reads_server_header(tcp_server):
    port = await tcp_server(fixture_bytes("nginx-http-head.bin"))
    result = await probes.http_probe("127.0.0.1", port, CTX)

    assert (result.state, result.version) == ("open", "nginx/1.28.3")
    assert result.details["status"] == 200


async def test_http_probe_non_http_service(tcp_server):
    port = await tcp_server(fixture_bytes("ssh-banner.bin"))
    result = await probes.http_probe("127.0.0.1", port, CTX)

    assert result.details == {"error": "not an HTTP response"}


async def test_http_probe_silent_service(tcp_server):
    port = await tcp_server(b"")
    result = await probes.http_probe("127.0.0.1", port, ProbeContext(timeout=0.2))

    assert result.details["error"].startswith("no response")


async def test_http_probe_closed_port():
    assert (await probes.http_probe("127.0.0.1", closed_port(), CTX)).state == "closed"


# --- TLS


def test_parse_real_lab_certificate():
    details = probes.parse_certificate(fixture_bytes("nginx-cert.der"))

    assert details["cert_subject"] == "CN=web.lab,O=netprobe lab"
    assert details["cert_sans"] == ["DNS:web.lab", "IP:172.30.57.13"]
    assert details["cert_self_signed"] is True
    assert details["cert_not_after"].endswith("+00:00")


def make_cert(tmp_path, *, sans=True):
    """Issue a CA and a leaf for 127.0.0.1; return (ca path, cert path, key path)."""
    now = dt.datetime.now(dt.UTC)
    ca_key = ec.generate_private_key(ec.SECP256R1())
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "netprobe test CA")])
    ca = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(1)
        .not_valid_before(now - dt.timedelta(minutes=5))
        .not_valid_after(now + dt.timedelta(days=1))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False
        )
        .sign(ca_key, hashes.SHA256())
    )
    key = ec.generate_private_key(ec.SECP256R1())
    builder = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")]))
        .issuer_name(ca_name)
        .public_key(key.public_key())
        .serial_number(2)
        .not_valid_before(now - dt.timedelta(minutes=5))
        .not_valid_after(now + dt.timedelta(days=1))
        # Python 3.13 verifies with VERIFY_X509_STRICT, which requires these.
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.ExtendedKeyUsage([x509.ExtendedKeyUsageOID.SERVER_AUTH]), critical=False
        )
    )
    if sans:
        builder = builder.add_extension(
            x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]),
            critical=False,
        )
    leaf = builder.sign(ca_key, hashes.SHA256())
    paths = tmp_path / "ca.pem", tmp_path / "leaf.pem", tmp_path / "leaf.key"
    paths[0].write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    paths[1].write_bytes(leaf.public_bytes(serialization.Encoding.PEM))
    paths[2].write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    return paths


@pytest.fixture
async def tls_server(tmp_path):
    servers = []

    async def start(sans=True):
        ca, cert, key = make_cert(tmp_path, sans=sans)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(cert, key)

        async def handle(reader, writer):
            try:
                await reader.readuntil(b"\r\n\r\n")
                writer.write(fixture_bytes("nginx-https-head.bin"))
                await writer.drain()
            except (asyncio.IncompleteReadError, ConnectionError, ssl.SSLError):
                pass
            writer.close()

        server = await asyncio.start_server(handle, "127.0.0.1", 0, ssl=context)
        servers.append(server)
        return server.sockets[0].getsockname()[1], str(ca)

    yield start
    for server in servers:
        server.close()


async def test_https_probe_verifies_against_given_ca(tls_server):
    port, ca = await tls_server()
    result = await probes.https_probe("127.0.0.1", port, ProbeContext(1.0, tls_ca_file=ca))

    assert result.state == "open"
    assert result.version == "nginx/1.28.3"
    assert result.details["cert_verified"] is True
    assert "cert_verify_error" not in result.details
    assert "cert_read_unverified" not in result.details
    assert result.details["cert_issuer"] == "CN=netprobe test CA"
    assert result.details["cert_sans"] == ["IP:127.0.0.1"]
    assert result.details["tls_version"].startswith("TLS")


async def test_https_probe_records_failed_verification(tls_server):
    port, _ = await tls_server()
    result = await probes.https_probe("127.0.0.1", port, CTX)

    assert result.details["cert_verified"] is False
    assert "cert_read_unverified" not in result.details
    assert "unable to get local issuer certificate" in result.details["cert_verify_error"]
    assert "cert_subject" not in result.details
    assert "server" not in result.details
    assert result.version == ""


async def test_https_probe_hostname_mismatch(tls_server):
    port, ca = await tls_server(sans=False)
    result = await probes.https_probe("127.0.0.1", port, ProbeContext(1.0, tls_ca_file=ca))

    assert result.details["cert_verified"] is False
    assert "mismatch" in result.details["cert_verify_error"].lower()
    assert "cert_sans" not in result.details


async def test_https_probe_plain_tcp_service(tcp_server):
    port = await tcp_server(fixture_bytes("ssh-banner.bin"))
    result = await probes.https_probe("127.0.0.1", port, CTX)

    assert result.state == "open"
    assert "tls_error" in result.details


async def test_https_probe_closed_port():
    assert (await probes.https_probe("127.0.0.1", closed_port(), CTX)).state == "closed"


async def test_https_probe_verification_failure_never_retries(monkeypatch):
    calls = []

    async def fake_open(host, port, timeout, tls=None):
        calls.append(tls)
        if len(calls) == 1:
            error = ssl.SSLCertVerificationError("verify failed")
            error.verify_message = "certificate has expired"
            raise error
        raise ssl.SSLError("handshake failure")

    monkeypatch.setattr(probes, "_open", fake_open)
    result = await probes.https_probe("127.0.0.1", 443, CTX)

    assert result.details["cert_verified"] is False
    assert result.details["cert_verify_error"] == "certificate has expired"
    assert len(calls) == 1
    assert calls[0].verify_mode == ssl.CERT_REQUIRED
    assert calls[0].check_hostname is True


# --- SNMP with credentials


async def test_snmp_probe_without_credentials_reports_engine(udp_server):
    port, _ = await udp_server(fixture_bytes("snmpv3-report.bin"))
    result = await probes.snmp_probe("127.0.0.1", port, CTX)

    assert result.state == "open"
    assert result.details == {"engine_id": "80001f88808aa1f93d7edcc66a00000000"}


async def test_snmp_probe_with_credentials_adds_system_mib(udp_server, monkeypatch):
    port, _ = await udp_server(b"")  # a v2c-only agent ignores v3 discovery
    seen = []

    async def fake_system(host, port, creds, timeout):
        seen.append(creds)
        return {
            "sys_descr": "Linux lab",
            "sys_object_id": "1.3.6.1.4.1.8072.3.2.10",
            "sys_name": "lab",
        }

    monkeypatch.setattr(probes, "snmp_system", fake_system)
    creds = SnmpCredentials(community="s3cret")
    result = await probes.snmp_probe("127.0.0.1", port, ProbeContext(0.1, snmp=creds))

    assert (result.state, result.version) == ("open", "Linux lab")
    assert result.details["snmp_version"] == "2c"
    assert result.details["sys_name"] == "lab"
    assert seen == [creds]


async def test_snmp_probe_get_failure_keeps_discovery_state(udp_server, monkeypatch):
    port, _ = await udp_server(fixture_bytes("snmpv3-report.bin"))

    async def failing(*args):
        raise RuntimeError("Wrong SNMP PDU digest")

    monkeypatch.setattr(probes, "snmp_system", failing)
    creds = SnmpCredentials(user="netprobe", auth_key="k" * 10)
    result = await probes.snmp_probe("127.0.0.1", port, ProbeContext(1.0, snmp=creds))

    assert result.state == "open"
    assert result.details["snmp_error"] == "Wrong SNMP PDU digest"


@pytest.mark.parametrize(
    "creds",
    [
        SnmpCredentials(community="s3cret"),
        SnmpCredentials(
            user="u",
            auth_key="authpass1",
            priv_key="privpass1",
            auth_protocol="SHA256",
            priv_protocol="AES256",
        ),
        SnmpCredentials(user="u"),
    ],
)
async def test_snmp_system_times_out_against_silent_agent(udp_server, creds):
    port, _ = await udp_server(b"")
    with pytest.raises(RuntimeError, match="No SNMP response"):
        await probes.snmp_system("127.0.0.1", port, creds, 0.2)


def test_credentials_repr_hides_secrets():
    v2c = SnmpCredentials(community="c0mm")
    v3 = SnmpCredentials(user="u", auth_key="a-key-1", priv_key="p-key-1")

    assert "c0mm" not in repr(v2c)
    assert "a-key-1" not in repr(v3)
    assert "p-key-1" not in repr(v3)
    assert (v2c.version, v3.version) == ("2c", "3")


@pytest.mark.parametrize(
    ("kwargs", "level"),
    [
        ({"user": "u"}, "noAuthNoPriv"),
        ({"user": "u", "auth_key": "authpass1"}, "authNoPriv"),
        ({"user": "u", "auth_key": "authpass1", "priv_key": "privpass1"}, "authPriv"),
        ({"community": "c"}, ""),
    ],
)
def test_security_level_matches_configuration(kwargs, level):
    assert SnmpCredentials(**kwargs).security_level == level


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"community": "c", "user": "u"}, "not both"),
        ({"user": "u", "priv_key": "privpass1"}, "needs an authentication key"),
        ({"auth_key": "authpass1"}, "need an SNMPv3 user"),
        ({"user": "u", "auth_protocol": "CRC"}, "auth protocol"),
        ({"user": "u", "priv_protocol": "ROT13"}, "privacy protocol"),
    ],
)
def test_credentials_refuse_ambiguity_and_downgrades(kwargs, message):
    with pytest.raises(ValueError, match=message):
        SnmpCredentials(**kwargs)


def test_redact_removes_every_secret():
    creds = SnmpCredentials(user="u", auth_key="authpass1", priv_key="privpass1")
    assert creds.redact("bad key authpass1 / privpass1") == "bad key *** / ***"


async def test_snmp_error_text_is_redacted(udp_server, monkeypatch):
    port, _ = await udp_server(b"")

    async def leaky(host, port, creds, timeout):
        raise RuntimeError(f"agent rejected community {creds.community}")

    monkeypatch.setattr(probes, "snmp_system", leaky)
    creds = SnmpCredentials(community="s3cret-c")
    result = await probes.snmp_probe("127.0.0.1", port, ProbeContext(0.1, snmp=creds))

    assert result.details["snmp_error"] == "agent rejected community ***"


async def test_v3_failure_is_never_retried_with_weaker_settings(udp_server, monkeypatch):
    port, _ = await udp_server(b"")
    attempts = []

    async def failing(host, port, creds, timeout):
        attempts.append(creds)
        raise RuntimeError("Wrong SNMP PDU digest")

    monkeypatch.setattr(probes, "snmp_system", failing)
    creds = SnmpCredentials(user="u", auth_key="authpass1", priv_key="privpass1")
    result = await probes.snmp_probe("127.0.0.1", port, ProbeContext(0.1, snmp=creds))

    assert attempts == [creds]
    assert result.state == "filtered"
    assert "snmp_version" not in result.details
    assert "sys_descr" not in result.details


async def test_mysql_probe_refuses_oversized_greeting(tcp_server):
    port = await tcp_server(b"\xff\xff\xff\x00" + b"x" * 64)
    result = await probes.mysql_probe("127.0.0.1", port, CTX)

    assert "too large" in result.details["error"]


async def test_ssh_probe_caps_line_length(tcp_server):
    port = await tcp_server(b"A" * (probes.MAX_LINE_BYTES * 4))
    result = await probes.ssh_probe("127.0.0.1", port, CTX)

    assert result.state == "open"
    assert result.details["error"].startswith("no banner")
