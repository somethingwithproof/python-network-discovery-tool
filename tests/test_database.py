"""
Tests for the database module.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Database, Exporter, Importer
from devices import Device


class TestDatabase:
    """Tests for the Database class."""

    def test_create_table(self, temp_database: Database):
        """Test table creation."""
        # Table should already exist from fixture
        devices = temp_database.get_all_devices()
        assert isinstance(devices, list)
        assert len(devices) == 0

    def test_create_table_drop_existing(self, temp_database: Database, sample_device: Device):
        """Test dropping existing table."""
        # Insert a device
        temp_database.insert_device(sample_device)
        assert len(temp_database.get_all_devices()) == 1

        # Drop and recreate
        temp_database.create_table(drop_existing=True)
        assert len(temp_database.get_all_devices()) == 0

    def test_insert_device(self, temp_database: Database, sample_device: Device):
        """Test inserting a device."""
        device_id = temp_database.insert_device(sample_device)
        assert device_id > 0

        devices = temp_database.get_all_devices()
        assert len(devices) == 1
        assert devices[0].host == sample_device.host

    def test_insert_multiple_devices(self, temp_database: Database, sample_devices: list[Device]):
        """Test inserting multiple devices."""
        for device in sample_devices:
            temp_database.insert_device(device)

        devices = temp_database.get_all_devices()
        assert len(devices) == len(sample_devices)

    def test_get_device(self, temp_database: Database, sample_device: Device):
        """Test retrieving a single device."""
        device_id = temp_database.insert_device(sample_device)

        device = temp_database.get_device(device_id)
        assert device is not None
        assert device.host == sample_device.host

    def test_get_device_not_found(self, temp_database: Database):
        """Test retrieving non-existent device."""
        device = temp_database.get_device(999)
        assert device is None

    def test_update_device(self, temp_database: Database, sample_device: Device):
        """Test updating a device."""
        device_id = temp_database.insert_device(sample_device)

        # Retrieve and modify
        device = temp_database.get_device(device_id)
        device.alive = True
        device.ssh = True
        device.uname = "Linux test 5.4.0"

        temp_database.update_device(device)

        # Verify update
        updated = temp_database.get_device(device_id)
        assert updated.alive is True
        assert updated.ssh is True
        assert updated.uname == "Linux test 5.4.0"

    def test_delete_device(self, temp_database: Database, sample_device: Device):
        """Test deleting a device."""
        device_id = temp_database.insert_device(sample_device)
        assert temp_database.get_device(device_id) is not None

        result = temp_database.delete_device(device_id)
        assert result is True
        assert temp_database.get_device(device_id) is None

    def test_delete_device_not_found(self, temp_database: Database):
        """Test deleting non-existent device."""
        result = temp_database.delete_device(999)
        assert result is False

    def test_get_all_devices_ordered(self, temp_database: Database):
        """Test that devices are returned ordered by ID."""
        devices = [
            Device(id=0, host="192.168.1.3", ip="192.168.1.3"),
            Device(id=0, host="192.168.1.1", ip="192.168.1.1"),
            Device(id=0, host="192.168.1.2", ip="192.168.1.2"),
        ]
        for device in devices:
            temp_database.insert_device(device)

        result = temp_database.get_all_devices()
        # Should be ordered by ID (insertion order)
        ids = [d.id for d in result]
        assert ids == sorted(ids)


class TestExporter:
    """Tests for the Exporter class."""

    def test_to_csv(self, sample_devices: list[Device], temp_dir: Path):
        """Test exporting devices to CSV."""
        # Mark devices as scanned
        for device in sample_devices:
            device.scanned = True
            device.alive = True

        exporter = Exporter(sample_devices)
        csv_path = temp_dir / "devices.csv"
        exporter.to_csv(csv_path)

        assert csv_path.exists()
        content = csv_path.read_text()
        assert "host" in content
        assert "192.168.1.1" in content

    def test_to_csv_with_errors(self, sample_device: Device, temp_dir: Path):
        """Test CSV export handles errors correctly."""
        sample_device.add_error("Test error 1")
        sample_device.add_error("Test error 2")

        exporter = Exporter([sample_device])
        csv_path = temp_dir / "devices.csv"
        exporter.to_csv(csv_path)

        content = csv_path.read_text()
        assert "Test error 1" in content

    def test_to_html_missing_template(self, sample_devices: list[Device], temp_dir: Path):
        """Test HTML export fails gracefully with missing template."""
        exporter = Exporter(sample_devices, template_dir=temp_dir / "nonexistent")

        with pytest.raises(FileNotFoundError):
            exporter.to_html(temp_dir / "output.html")


class TestImporter:
    """Tests for the Importer class."""

    def test_from_csv(self, temp_database: Database, sample_csv_file: Path):
        """Test importing devices from CSV."""
        importer = Importer(temp_database)
        count = importer.from_csv(sample_csv_file)

        assert count == 2
        devices = temp_database.get_all_devices()
        assert len(devices) == 2

    def test_from_csv_with_credentials(self, temp_database: Database, sample_csv_file: Path):
        """Test that CSV import includes MySQL credentials."""
        importer = Importer(temp_database)
        importer.from_csv(sample_csv_file)

        devices = temp_database.get_all_devices()
        admin_device = next(d for d in devices if d.mysql_user == "admin")
        assert admin_device is not None


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    def test_create(self, temp_dir: Path):
        """Test create convenience function."""
        from database import create

        db_path = temp_dir / "test.db"
        db = create(db_path)

        assert db_path.exists()
        assert len(db.get_all_devices()) == 0

    def test_get_all_devices(self, temp_dir: Path, sample_device: Device):
        """Test get_all_devices convenience function."""
        from database import create, get_all_devices

        db_path = temp_dir / "test.db"
        db = create(db_path)
        db.insert_device(sample_device)

        devices = get_all_devices(db_path)
        assert len(devices) == 1

    def test_update_device(self, temp_dir: Path, sample_device: Device):
        """Test update_device convenience function."""
        from database import create
        from database import update_device as db_update

        db_path = temp_dir / "test.db"
        db = create(db_path)
        device_id = db.insert_device(sample_device)

        device = db.get_device(device_id)
        device.alive = True
        db_update(db_path, device)

        updated = db.get_device(device_id)
        assert updated.alive is True
