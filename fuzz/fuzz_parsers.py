# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Bounded, offline fuzzing of untrusted service responses; no sockets or secrets."""

from __future__ import annotations

import contextlib
import sys

import atheris

with atheris.instrument_imports():
    from hostcensus.probes import (
        MAX_ENGINE_ID_OCTETS,
        parse_certificate,
        parse_http_head,
        parse_mysql_handshake,
        parse_ssh_banner,
        snmp_engine_id,
    )

HEX_DIGITS = frozenset("0123456789abcdef")


@atheris.instrument_func
def fuzz_one_input(data: bytes) -> None:
    if not data:
        return
    selector, payload = data[0] % 5, data[1:4097]
    if selector == 0:
        parse_ssh_banner(payload)
    elif selector == 1:
        parse_mysql_handshake(payload)
    elif selector == 2:
        parse_http_head(payload)
    elif selector == 3:
        # The BER walker must turn any malformed reply into None, never raise.
        engine_id = snmp_engine_id(payload)
        if engine_id is not None:
            assert 0 < len(engine_id) <= 2 * MAX_ENGINE_ID_OCTETS
            assert set(engine_id) <= HEX_DIGITS
    else:
        # DER decoding rejects malformed certificates by contract.
        with contextlib.suppress(ValueError):
            parse_certificate(payload)


def main() -> None:
    atheris.Setup(sys.argv, fuzz_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
