"""Tests for the ReportGenerator class."""

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from network_discovery.domain.device import Device
from network_discovery.infrastructure.report import ReportGenerator


@pytest.fixture
def report_generator():
    """Return a report generator instance."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield ReportGenerator(output_dir=temp_dir, template_dir="./templates")


@pytest.fixture
def devices():
    """Return a list of devices for testing."""
    return [
        Device(id=1, host="example1.com", ip="192.168.1.1", alive=True, ssh=True, snmp=False, mysql=True),
        Device(id=2, host="example2.com", ip="192.168.1.2", alive=True, ssh=False, snmp=True, mysql=False),
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

    def test_ensure_output_dir_exists(self):
        """Test that the output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, "output")
            assert not os.path.exists(output_dir)
            
            generator = ReportGenerator(output_dir=output_dir, template_dir="./templates")
            generator._ensure_output_dir_exists()
            
            assert os.path.exists(output_dir)

    def test_generate_html_report(self, report_generator, devices):
        """Test that an HTML report can be generated."""
        # Mock the jinja2.Environment
        with patch("jinja2.Environment") as mock_env:
            # Mock the get_template method
            mock_template = MagicMock()
            mock_env.return_value.get_template.return_value = mock_template
            
            # Mock the render method
            mock_template.render.return_value = "<html>Test Report</html>"
            
            # Generate the report
            report_path = report_generator.generate_html_report(devices)
            
            # Check that the template was loaded
            mock_env.return_value.get_template.assert_called_once_with("html_report.html")
            
            # Check that the template was rendered with the devices
            mock_template.render.assert_called_once()
            args, kwargs = mock_template.render.call_args
            assert "devices" in kwargs
            assert kwargs["devices"] == devices
            
            # Check that the report was written to a file
            assert os.path.exists(report_path)
            with open(report_path, "r", encoding="utf-8") as f:
                assert f.read() == "<html>Test Report</html>"

    def test_generate_csv_report(self, report_generator, devices):
        """Test that a CSV report can be generated."""
        # Generate the report
        report_path = report_generator.generate_csv_report(devices)
        
        # Check that the report was written to a file
        assert os.path.exists(report_path)
        
        # Check that the file contains the expected content
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "ID,Host,IP,Alive,SSH,SNMP,MySQL" in content
            assert "1,example1.com,192.168.1.1,True,True,False,True" in content
            assert "2,example2.com,192.168.1.2,True,False,True,False" in content
            assert "3,example3.com,192.168.1.3,False,False,False,False" in content

    def test_generate_json_report(self, report_generator, devices):
        """Test that a JSON report can be generated."""
        # Generate the report
        report_path = report_generator.generate_json_report(devices)
        
        # Check that the report was written to a file
        assert os.path.exists(report_path)
        
        # Check that the file contains valid JSON
        import json
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert len(data) == 3
            assert data[0]["id"] == 1
            assert data[0]["host"] == "example1.com"
            assert data[0]["ip"] == "192.168.1.1"
            assert data[0]["alive"] is True
            assert data[0]["ssh"] is True
            assert data[0]["snmp"] is False
            assert data[0]["mysql"] is True

    def test_generate_report_html(self, report_generator, devices):
        """Test that generate_report works with HTML format."""
        with patch.object(report_generator, "generate_html_report") as mock_html:
            mock_html.return_value = "/path/to/report.html"
            
            # Generate the report
            report_path = report_generator.generate_report(devices, "html")
            
            # Check that the HTML report was generated
            mock_html.assert_called_once_with(devices)
            assert report_path == "/path/to/report.html"

    def test_generate_report_csv(self, report_generator, devices):
        """Test that generate_report works with CSV format."""
        with patch.object(report_generator, "generate_csv_report") as mock_csv:
            mock_csv.return_value = "/path/to/report.csv"
            
            # Generate the report
            report_path = report_generator.generate_report(devices, "csv")
            
            # Check that the CSV report was generated
            mock_csv.assert_called_once_with(devices)
            assert report_path == "/path/to/report.csv"

    def test_generate_report_json(self, report_generator, devices):
        """Test that generate_report works with JSON format."""
        with patch.object(report_generator, "generate_json_report") as mock_json:
            mock_json.return_value = "/path/to/report.json"
            
            # Generate the report
            report_path = report_generator.generate_report(devices, "json")
            
            # Check that the JSON report was generated
            mock_json.assert_called_once_with(devices)
            assert report_path == "/path/to/report.json"

    def test_generate_report_invalid_format(self, report_generator, devices):
        """Test that generate_report raises a ValueError for invalid formats."""
        with pytest.raises(ValueError):
            report_generator.generate_report(devices, "invalid")

    def test_generate_report_empty_devices(self, report_generator):
        """Test that generate_report works with an empty list of devices."""
        # Generate the report
        report_path = report_generator.generate_report([], "html")
        
        # Check that the report was written to a file
        assert os.path.exists(report_path)
