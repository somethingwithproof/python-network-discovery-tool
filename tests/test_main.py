import runpy
from unittest.mock import patch

import pytest


def test_python_dash_m_runs_cli(capsys):
    with patch("sys.argv", ["netprobe", "version"]), pytest.raises(SystemExit) as exit_info:
        runpy.run_module("netprobe", run_name="__main__")

    assert exit_info.value.code == 0
    assert "netprobe" in capsys.readouterr().out
