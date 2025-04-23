"""Enterprise device module.

This module provides an enterprise-class device implementation with enhanced features.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Set, Tuple

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


@dataclass(frozen=True)
class EnterpriseDevice:
    """Enterprise-class device with enhanced features.

    This class uses composition to extend the base Device class with additional enterprise features
    such as asset management, compliance tracking, and enhanced monitoring capabilities.

    Attributes:
        device: The base Device object.
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
        compliance_issues: Tuple of compliance issues.
        tags: Frozenset of tags associated with the device.
        custom_attributes: Dictionary of custom attributes (immutable).
        last_scan_time: The time of the last scan.
        uptime: The uptime of the device in seconds.
        services: Dictionary of services running on the device (immutable).
    """

    device: Device
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
    compliance_issues: Tuple[str, ...] = field(default_factory=tuple)
    tags: frozenset = field(default_factory=frozenset)
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
    last_scan_time: Optional[datetime] = None
    uptime: Optional[int] = None
    services: Dict[str, bool] = field(default_factory=dict)

    def add_tag(self, tag: str) -> 'EnterpriseDevice':
        """Add a tag to the device.

        Args:
            tag: The tag to add.
            
        Returns:
            A new EnterpriseDevice instance with the tag added.
        """
        new_tags = set(self.tags)
        new_tags.add(tag)
        return self.replace(tags=frozenset(new_tags))

    def remove_tag(self, tag: str) -> 'EnterpriseDevice':
        """Remove a tag from the device.

        Args:
            tag: The tag to remove.
            
        Returns:
            A new EnterpriseDevice instance with the tag removed.
        """
        new_tags = set(self.tags)
        new_tags.discard(tag)
        return self.replace(tags=frozenset(new_tags))

    def set_custom_attribute(self, key: str, value: Any) -> 'EnterpriseDevice':
        """Set a custom attribute on the device.

        Args:
            key: The attribute key.
            value: The attribute value.
            
        Returns:
            A new EnterpriseDevice instance with the custom attribute set.
        """
        new_attributes = dict(self.custom_attributes)
        new_attributes[key] = value
        return self.replace(custom_attributes=new_attributes)

    def get_custom_attribute(self, key: str, default: Any = None) -> Any:
        """Get a custom attribute from the device.

        Args:
            key: The attribute key.
            default: The default value to return if the key is not found.

        Returns:
            The attribute value, or the default if not found.
        """
        return self.custom_attributes.get(key, default)

    def add_service(self, service_name: str, status: bool = True) -> 'EnterpriseDevice':
        """Add a service to the device.

        Args:
            service_name: The name of the service.
            status: The status of the service (True for running, False for stopped).
            
        Returns:
            A new EnterpriseDevice instance with the service added.
        """
        new_services = dict(self.services)
        new_services[service_name] = status
        return self.replace(services=new_services)

    def get_service_status(self, service_name: str) -> Optional[bool]:
        """Get the status of a service.

        Args:
            service_name: The name of the service.

        Returns:
            The status of the service, or None if the service is not found.
        """
        return self.services.get(service_name)

    def update_scan_time(self) -> 'EnterpriseDevice':
        """Update the last scan time to the current time.
        
        Returns:
            A new EnterpriseDevice instance with the updated scan time.
        """
        return self.replace(last_scan_time=datetime.now())

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
        base_dict = self.device.to_dict()
        
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
            "compliance_issues": list(self.compliance_issues),
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
        
        # Convert compliance issues to tuple
        compliance_issues = tuple(dict_device.get("compliance_issues", []))
        
        # Convert tags to frozenset
        tags = frozenset(dict_device.get("tags", []))
        
        # Create the enterprise device
        return cls(
            device=base_device,
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
            compliance_issues=compliance_issues,
            tags=tags,
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
        return f"{self.device.host} ({self.device.ip}) - {self.category.name} - {self.status.name}"
        
    def replace(self, **kwargs) -> 'EnterpriseDevice':
        """Create a new EnterpriseDevice with some fields replaced.
        
        Args:
            **kwargs: The fields to replace and their new values.
            
        Returns:
            A new EnterpriseDevice instance with the specified fields replaced.
        """
        # Create a dictionary of the current field values
        fields = {
            "device": self.device,
            "category": self.category,
            "status": self.status,
            "asset_id": self.asset_id,
            "location": self.location,
            "owner": self.owner,
            "purchase_date": self.purchase_date,
            "warranty_expiry": self.warranty_expiry,
            "last_patched": self.last_patched,
            "os_version": self.os_version,
            "firmware_version": self.firmware_version,
            "compliance": self.compliance,
            "compliance_issues": self.compliance_issues,
            "tags": self.tags,
            "custom_attributes": self.custom_attributes,
            "last_scan_time": self.last_scan_time,
            "uptime": self.uptime,
            "services": self.services,
        }
        
        # Update with the new values
        fields.update(kwargs)
        
        # Create a new EnterpriseDevice instance
        return EnterpriseDevice(**fields)
        
    # Delegate common Device methods and properties to the device attribute
    
    @property
    def id(self) -> int:
        """Get the device ID."""
        return self.device.id
        
    @property
    def host(self) -> str:
        """Get the device hostname."""
        return self.device.host
        
    @property
    def ip(self) -> str:
        """Get the device IP address."""
        return self.device.ip
        
    @property
    def alive(self) -> bool:
        """Get whether the device is alive."""
        return self.device.alive
        
    @property
    def ssh(self) -> bool:
        """Get whether SSH is available on the device."""
        return self.device.ssh
        
    @property
    def snmp(self) -> bool:
        """Get whether SNMP is available on the device."""
        return self.device.snmp
        
    @property
    def mysql(self) -> bool:
        """Get whether MySQL is available on the device."""
        return self.device.mysql
        
    @property
    def errors(self) -> Tuple[str, ...]:
        """Get the device errors."""
        return self.device.errors
        
    @property
    def scanned(self) -> bool:
        """Get whether the device has been scanned."""
        return self.device.scanned
        
    def status_summary(self) -> str:
        """Get a summary of the device's status."""
        return self.device.status()
