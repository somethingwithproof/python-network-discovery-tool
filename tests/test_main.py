# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

import runpy
from unittest.mock import patch

import pytest


def test_python_dash_m_runs_cli(capsys):
    with patch("sys.argv", ["hostcensus", "version"]), pytest.raises(SystemExit) as exit_info:
        runpy.run_module("hostcensus", run_name="__main__")

    assert exit_info.value.code == 0
    assert "hostcensus" in capsys.readouterr().out
