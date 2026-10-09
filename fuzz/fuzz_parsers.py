"""Bounded, offline fuzzing of untrusted service responses; no sockets or secrets."""

from __future__ import annotations

import contextlib
import sys

import atheris

with atheris.instrument_imports():
    from netprobe.probes import (
        parse_certificate,
        parse_http_head,
        parse_mysql_handshake,
        parse_ssh_banner,
    )


@atheris.instrument_func
def fuzz_one_input(data: bytes) -> None:
    if not data:
        return
    selector, payload = data[0] % 4, data[1:4097]
    if selector == 0:
        parse_ssh_banner(payload)
    elif selector == 1:
        parse_mysql_handshake(payload)
    elif selector == 2:
        parse_http_head(payload)
    else:
        # DER decoding rejects malformed certificates by contract.
        with contextlib.suppress(ValueError):
            parse_certificate(payload)


def main() -> None:
    atheris.Setup(sys.argv, fuzz_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
