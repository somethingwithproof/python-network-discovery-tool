"""Tests for the ReportGenerator class."""

import json
import tempfile
from pathlib import Path

import pytest

from network_discovery.domain.device import Device
from network_discovery.infrastructure.report import ReportGenerator


@pytest.fixture
def report_generator():
    """Return a report generator instance with a valid template directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        template_dir = Path(temp_dir) / "templates"
        template_dir.mkdir()
        (template_dir / "layout.html").write_text("""<!DOCTYPE html>
<html>
<head><title>Device Report</title></head>
<body>
<h1>Device Report</h1>
<p>Generated: {{ generated_at }}</p>
<p>Total: {{ total_devices }}, Alive: {{ alive_devices }}</p>
<ul>
{% for device in devices %}
<li>{{ device.host }} ({{ device.ip }}) - Alive: {{ device.alive }}</li>
{% endfor %}
</ul>
</body>
</html>""")

        output_dir = str(Path(temp_dir) / "output")
        yield ReportGenerator(output_dir=output_dir, template_dir=str(template_dir))


@pytest.fixture
def devices():
    """Return a list of devices for testing."""
    return [
        Device(
            id=1,
            host="example1.com",
            ip="192.168.1.1",
            alive=True,
            ssh=True,
            snmp=False,
            mysql=True,
        ),
        Device(
            id=2,
            host="example2.com",
            ip="192.168.1.2",
            alive=True,
            ssh=False,
            snmp=True,
            mysql=False,
        ),
        Device(id=3, host="example3.com", ip="192.168.1.3", alive=False),
    ]


class TestReportGenerator:
    """Tests for the ReportGenerator class."""

    def test_init(self):
        """Test that a ReportGenerator can be initialized."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = ReportGenerator(output_dir=temp_dir, template_dir="./templates")
            assert generator.output_dir == temp_dir
            assert generator.template_dir == "./templates"

    def test_init_creates_output_dir(self):
        """Test that the output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = str(Path(temp_dir) / "output")
            assert not Path(output_dir).exists()

            ReportGenerator(output_dir=output_dir, template_dir="./templates")

            assert Path(output_dir).exists()

    def test_supported_formats(self, report_generator):
        """Test that supported formats are returned."""
        formats = report_generator.supported_formats
        assert "html" in formats
        assert "csv" in formats
        assert "xlsx" in formats
        assert "json" in formats

    def test_generate_html_report(self, report_generator, devices):
        """Test that an HTML report can be generated."""
        report_path = report_generator.generate_report(devices, "html")

        assert Path(report_path).exists()
        assert report_path.endswith(".html")

        content = Path(report_path).read_text(encoding="utf-8")
        assert "Device Report" in content
        assert "example1.com" in content
        assert "192.168.1.1" in content

    def test_generate_csv_report(self, report_generator, devices):
        """Test that a CSV report can be generated."""
        report_path = report_generator.generate_report(devices, "csv")

        assert Path(report_path).exists()
        assert report_path.endswith(".csv")

        content = Path(report_path).read_text(encoding="utf-8")
        assert "ID,Host,IP" in content
        assert "1,example1.com,192.168.1.1" in content
        assert "2,example2.com,192.168.1.2" in content
        assert "3,example3.com,192.168.1.3" in content

    def test_generate_json_report(self, report_generator, devices):
        """Test that a JSON report can be generated."""
        report_path = report_generator.generate_report(devices, "json")

        assert Path(report_path).exists()
        assert report_path.endswith(".json")

        with Path(report_path).open(encoding="utf-8") as f:
            data = json.load(f)
            assert "metadata" in data
            assert "devices" in data
            assert "summary" in data

            assert data["metadata"]["total_devices"] == 3
            assert len(data["devices"]) == 3
            assert data["devices"][0]["id"] == 1
            assert data["devices"][0]["host"] == "example1.com"

    def test_generate_xlsx_report(self, report_generator, devices):
        """Test that an Excel report can be generated."""
        report_path = report_generator.generate_report(devices, "xlsx")

        assert Path(report_path).exists()
        assert report_path.endswith(".xlsx")

    def test_generate_report_with_custom_filename(self, report_generator, devices):
        """Test that generate_report works with a custom filename."""
        report_path = report_generator.generate_report(
            devices, "csv", filename="custom_report"
        )

        assert Path(report_path).exists()
        assert "custom_report.csv" in report_path

    def test_generate_report_invalid_format(self, report_generator, devices):
        """Test that generate_report raises a ValueError for invalid formats."""
        with pytest.raises(ValueError) as exc_info:
            report_generator.generate_report(devices, "invalid")
        assert "Unsupported report format" in str(exc_info.value)

    def test_generate_report_empty_devices(self, report_generator):
        """Test that generate_report works with an empty list of devices."""
        report_path = report_generator.generate_report([], "html")
        assert Path(report_path).exists()

    def test_generate_report_formats_case_insensitive(self, report_generator, devices):
        """Test that format type is case insensitive."""
        report_path = report_generator.generate_report(devices, "CSV")
        assert Path(report_path).exists()
        assert report_path.endswith(".csv")

    def test_export_all_formats(self, report_generator, devices):
        """Test that all formats can be exported at once."""
        results = report_generator.export_all_formats(devices, filename="all_formats")

        assert "html" in results
        assert "csv" in results
        assert "xlsx" in results
        assert "json" in results

        for _format_type, path in results.items():
            if path is not None:
                assert Path(path).exists()

    def test_html_report_requires_template_dir(self):
        """Test that HTML report requires a template directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = ReportGenerator(output_dir=temp_dir, template_dir=None)

            with pytest.raises(ValueError) as exc_info:
                generator.generate_report([], "html")
            assert "Template directory is required" in str(exc_info.value)
