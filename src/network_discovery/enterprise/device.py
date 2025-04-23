"""Enterprise device module.

This module provides an enterprise-class device implementation with enhanced features.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Set

from network_discovery.domain.device import Device


class DeviceCategory(Enum):
    """Enumeration of device categories."""

    NETWORK = auto()
    SERVER = auto()
    STORAGE = auto()
    SECURITY = auto()
    ENDPOINT = auto()
    VIRTUAL = auto()
    IOT = auto()
    UNKNOWN = auto()


class DeviceStatus(Enum):
    """Enumeration of device operational statuses."""

    OPERATIONAL = auto()
    DEGRADED = auto()
    MAINTENANCE = auto()
    CRITICAL = auto()
    UNKNOWN = auto()


@dataclass
class EnterpriseDevice(Device):
    """Enterprise-class device with enhanced features.

    This class extends the base Device class with additional enterprise features
    such as asset management, compliance tracking, and enhanced monitoring capabilities.

    Attributes:
        category: The category of the device.
        status: The operational status of the device.
        asset_id: The asset ID of the device.
        location: The physical location of the device.
        owner: The owner or responsible team for the device.
        purchase_date: The date the device was purchased.
        warranty_expiry: The date the warranty expires.
        last_patched: The date the device was last patched.
        os_version: The operating system version.
        firmware_version: The firmware version.
        compliance: Whether the device is compliant with security policies.
        compliance_issues: List of compliance issues.
        tags: Set of tags associated with the device.
        custom_attributes: Dictionary of custom attributes.
        last_scan_time: The time of the last scan.
        uptime: The uptime of the device in seconds.
        services: Dictionary of services running on the device.
    """

    category: DeviceCategory = DeviceCategory.UNKNOWN
    status: DeviceStatus = DeviceStatus.UNKNOWN
    asset_id: str = ""
    location: str = ""
    owner: str = ""
    purchase_date: Optional[datetime] = None
    warranty_expiry: Optional[datetime] = None
    last_patched: Optional[datetime] = None
    os_version: str = ""
    firmware_version: str = ""
    compliance: bool = False
    compliance_issues: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
    last_scan_time: Optional[datetime] = None
    uptime: Optional[int] = None
    services: Dict[str, bool] = field(default_factory=dict)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the device.

        Args:
            tag: The tag to add.
        """
        self.tags.add(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the device.

        Args:
            tag: The tag to remove.
        """
        self.tags.discard(tag)

    def set_custom_attribute(self, key: str, value: Any) -> None:
        """Set a custom attribute on the device.

        Args:
            key: The attribute key.
            value: The attribute value.
        """
        self.custom_attributes[key] = value

    def get_custom_attribute(self, key: str, default: Any = None) -> Any:
        """Get a custom attribute from the device.

        Args:
            key: The attribute key.
            default: The default value to return if the key is not found.

        Returns:
            The attribute value, or the default if not found.
        """
        return self.custom_attributes.get(key, default)

    def add_service(self, service_name: str, status: bool = True) -> None:
        """Add a service to the device.

        Args:
            service_name: The name of the service.
            status: The status of the service (True for running, False for stopped).
        """
        self.services[service_name] = status

    def get_service_status(self, service_name: str) -> Optional[bool]:
        """Get the status of a service.

        Args:
            service_name: The name of the service.

        Returns:
            The status of the service, or None if the service is not found.
        """
        return self.services.get(service_name)

    def update_scan_time(self) -> None:
        """Update the last scan time to the current time."""
        self.last_scan_time = datetime.now()

    def days_since_patched(self) -> Optional[int]:
        """Calculate the number of days since the device was last patched.

        Returns:
            The number of days since the last patch, or None if the last patch date is unknown.
        """
        if self.last_patched is None:
            return None
        delta = datetime.now() - self.last_patched
        return delta.days

    def days_until_warranty_expiry(self) -> Optional[int]:
        """Calculate the number of days until the warranty expires.

        Returns:
            The number of days until warranty expiry, or None if the warranty expiry date is unknown.
            A negative value indicates the warranty has already expired.
        """
        if self.warranty_expiry is None:
            return None
        delta = self.warranty_expiry - datetime.now()
        return delta.days

    def to_dict(self) -> Dict[str, Any]:
        """Convert the device attributes to a dictionary.

        Returns:
            A dictionary representation of the device.
        """
        base_dict = super().to_dict()
        
        # Add enterprise-specific attributes
        enterprise_dict = {
            "category": self.category.name,
            "status": self.status.name,
            "asset_id": self.asset_id,
            "location": self.location,
            "owner": self.owner,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
            "warranty_expiry": self.warranty_expiry.isoformat() if self.warranty_expiry else None,
            "last_patched": self.last_patched.isoformat() if self.last_patched else None,
            "os_version": self.os_version,
            "firmware_version": self.firmware_version,
            "compliance": self.compliance,
            "compliance_issues": self.compliance_issues,
            "tags": list(self.tags),
            "custom_attributes": self.custom_attributes,
            "last_scan_time": self.last_scan_time.isoformat() if self.last_scan_time else None,
            "uptime": self.uptime,
            "services": self.services,
        }
        
        # Merge dictionaries
        return {**base_dict, **enterprise_dict}

    @classmethod
    def from_dict(cls, dict_device: Dict[str, Any]) -> "EnterpriseDevice":
        """Create an EnterpriseDevice object from a dictionary.

        Args:
            dict_device: A dictionary containing device attributes.

        Returns:
            A new EnterpriseDevice instance.
        """
        # Create a base Device first
        base_device = Device.from_dict(dict_device)
        
        # Parse dates
        purchase_date = None
        if dict_device.get("purchase_date"):
            purchase_date = datetime.fromisoformat(dict_device["purchase_date"])
            
        warranty_expiry = None
        if dict_device.get("warranty_expiry"):
            warranty_expiry = datetime.fromisoformat(dict_device["warranty_expiry"])
            
        last_patched = None
        if dict_device.get("last_patched"):
            last_patched = datetime.fromisoformat(dict_device["last_patched"])
            
        last_scan_time = None
        if dict_device.get("last_scan_time"):
            last_scan_time = datetime.fromisoformat(dict_device["last_scan_time"])
        
        # Parse enums
        category = DeviceCategory.UNKNOWN
        if dict_device.get("category"):
            try:
                category = DeviceCategory[dict_device["category"]]
            except (KeyError, ValueError):
                pass
                
        status = DeviceStatus.UNKNOWN
        if dict_device.get("status"):
            try:
                status = DeviceStatus[dict_device["status"]]
            except (KeyError, ValueError):
                pass
        
        # Create the enterprise device
        return cls(
            id=base_device.id,
            host=base_device.host,
            ip=base_device.ip,
            snmp_group=base_device.snmp_group,
            alive=base_device.alive,
            snmp=base_device.snmp,
            ssh=base_device.ssh,
            mysql=base_device.mysql,
            mysql_user=base_device.mysql_user,
            mysql_password=base_device.mysql_password,
            uname=base_device.uname,
            errors=base_device.errors,
            scanned=base_device.scanned,
            category=category,
            status=status,
            asset_id=dict_device.get("asset_id", ""),
            location=dict_device.get("location", ""),
            owner=dict_device.get("owner", ""),
            purchase_date=purchase_date,
            warranty_expiry=warranty_expiry,
            last_patched=last_patched,
            os_version=dict_device.get("os_version", ""),
            firmware_version=dict_device.get("firmware_version", ""),
            compliance=dict_device.get("compliance", False),
            compliance_issues=dict_device.get("compliance_issues", []),
            tags=set(dict_device.get("tags", [])),
            custom_attributes=dict_device.get("custom_attributes", {}),
            last_scan_time=last_scan_time,
            uptime=dict_device.get("uptime"),
            services=dict_device.get("services", {}),
        )

    def __str__(self) -> str:
        """Return a string representation of the device.

        Returns:
            A string representation of the device.
        """
        return f"{self.host} ({self.ip}) - {self.category.name} - {self.status.name}"
