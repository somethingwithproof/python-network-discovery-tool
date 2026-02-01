"""REST API for Network Discovery Tool.

This module provides a FastAPI-based REST API for triggering scans,
retrieving results, and managing device discovery.

Features:
- Async scan operations
- Real-time status updates
- Device CRUD operations
- Report generation
- WebSocket support for live updates
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from network_discovery.core.discovery import DeviceDiscoveryService
from network_discovery.domain.device import Device
from network_discovery.infrastructure.report import ReportGenerator
from network_discovery.infrastructure.repository import JsonFileRepository
from network_discovery.infrastructure.scanner import NmapDeviceScanner, RateLimiter


logger = logging.getLogger(__name__)

# Global state for scan jobs
scan_jobs: dict[str, dict[str, Any]] = {}


# Pydantic models for API
class DeviceCreate(BaseModel):
    """Model for creating a new device."""

    host: str = Field(..., description="Hostname or IP address")
    ip: str = Field(..., description="IP address")
    snmp_group: str = Field(default="public", description="SNMP community string")
    mysql_user: str = Field(default="", description="MySQL username")
    mysql_password: str = Field(default="", description="MySQL password")
    snmp_version: int = Field(default=2, ge=1, le=3, description="SNMP version")
    snmpv3_user: str = Field(default="", description="SNMPv3 username")
    snmpv3_auth_protocol: str = Field(default="", description="SNMPv3 auth protocol")
    snmpv3_auth_password: str = Field(default="", description="SNMPv3 auth password")
    snmpv3_priv_protocol: str = Field(default="", description="SNMPv3 priv protocol")
    snmpv3_priv_password: str = Field(default="", description="SNMPv3 priv password")
    custom_ports: list[tuple[str, int]] = Field(
        default_factory=list, description="Custom port mappings"
    )


class DeviceResponse(BaseModel):
    """Model for device response."""

    id: int
    host: str
    ip: str
    snmp_group: str
    alive: bool
    snmp: bool
    ssh: bool
    mysql: bool
    http: bool
    https: bool
    uname: str
    os_fingerprint: str
    server_headers: str
    ssl_info: str
    snmp_version: int
    errors: list[str]
    scanned: bool

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class ScanRequest(BaseModel):
    """Model for scan request."""

    network: str = Field(
        ..., description="Network CIDR (e.g., '192.168.1.0/24') or single IP"
    )
    enable_os_detection: bool = Field(
        default=False, description="Enable OS fingerprinting (requires root)"
    )
    max_concurrent: int = Field(
        default=10, ge=1, le=100, description="Max concurrent scans"
    )
    rate_limit: float = Field(
        default=5.0, ge=0.1, le=100.0, description="Scans per second"
    )


class ScanStatus(BaseModel):
    """Model for scan job status."""

    job_id: str
    status: str  # pending, running, completed, failed
    network: str
    total_devices: int
    scanned_devices: int
    started_at: str | None
    completed_at: str | None
    error: str | None


class ReportRequest(BaseModel):
    """Model for report generation request."""

    format: str = Field(
        default="json",
        description="Report format: json, csv, xlsx, html, pdf",
    )
    mask_sensitive: bool = Field(
        default=True, description="Mask sensitive data in reports"
    )


# Application state
class AppState:
    """Application state container."""

    def __init__(self) -> None:
        """Initialize application state."""
        self.repository: JsonFileRepository | None = None
        self.scanner: NmapDeviceScanner | None = None
        self.discovery: DeviceDiscoveryService | None = None
        self.report_generator: ReportGenerator | None = None

    def initialize(
        self,
        repository_path: Path | None = None,
        template_dir: Path | None = None,
        report_output_dir: Path | None = None,
    ) -> None:
        """Initialize services.

        Args:
            repository_path: Path to JSON repository file.
            template_dir: Path to HTML templates directory.
            report_output_dir: Path to directory for generated reports.
        """
        repo_path = repository_path or Path("devices.json")
        output_dir = str(report_output_dir or Path("./reports"))
        self.repository = JsonFileRepository(repo_path)
        self.scanner = NmapDeviceScanner()
        self.discovery = DeviceDiscoveryService(
            scanner=self.scanner,
            repository=self.repository,
        )
        if template_dir:
            self.report_generator = ReportGenerator(
                output_dir=output_dir, template_dir=str(template_dir)
            )
        else:
            self.report_generator = ReportGenerator(output_dir=output_dir)


app_state = AppState()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    app_state.initialize()
    logger.info("API services initialized")
    yield
    # Shutdown
    logger.info("API shutting down")


# Create FastAPI app
app = FastAPI(
    title="Network Discovery API",
    description="REST API for network device discovery and monitoring",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "network-discovery-api"}


# Device endpoints
@app.get("/api/v1/devices", tags=["Devices"])
async def list_devices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    mask_sensitive: bool = Query(True),
) -> list[dict[str, Any]]:
    """List all discovered devices.

    Args:
        skip: Number of devices to skip.
        limit: Maximum number of devices to return.
        mask_sensitive: Mask sensitive data like passwords.

    Returns:
        List of device dictionaries.
    """
    if not app_state.repository:
        raise HTTPException(status_code=500, detail="Repository not initialized")

    devices = app_state.repository.get_all()
    paginated = devices[skip : skip + limit]

    return [d.to_dict(mask_sensitive=mask_sensitive) for d in paginated]


@app.get("/api/v1/devices/{device_id}", tags=["Devices"])
async def get_device(
    device_id: int, mask_sensitive: bool = Query(True)
) -> dict[str, Any]:
    """Get a specific device by ID.

    Args:
        device_id: The device ID.
        mask_sensitive: Mask sensitive data like passwords.

    Returns:
        Device dictionary.
    """
    if not app_state.repository:
        raise HTTPException(status_code=500, detail="Repository not initialized")

    device = app_state.repository.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device.to_dict(mask_sensitive=mask_sensitive)


@app.post("/api/v1/devices", tags=["Devices"], status_code=201)
async def create_device(device_data: DeviceCreate) -> dict[str, Any]:
    """Create a new device entry.

    Args:
        device_data: Device creation data.

    Returns:
        Created device dictionary.
    """
    if not app_state.repository:
        raise HTTPException(status_code=500, detail="Repository not initialized")

    # Generate new ID
    existing = app_state.repository.get_all()
    new_id = max([d.id for d in existing], default=0) + 1

    device = Device(
        id=new_id,
        host=device_data.host,
        ip=device_data.ip,
        snmp_group=device_data.snmp_group,
        mysql_user=device_data.mysql_user,
        mysql_password=device_data.mysql_password,
        snmp_version=device_data.snmp_version,
        snmpv3_user=device_data.snmpv3_user,
        snmpv3_auth_protocol=device_data.snmpv3_auth_protocol,
        snmpv3_auth_password=device_data.snmpv3_auth_password,
        snmpv3_priv_protocol=device_data.snmpv3_priv_protocol,
        snmpv3_priv_password=device_data.snmpv3_priv_password,
        custom_ports=tuple(tuple(p) for p in device_data.custom_ports),
    )

    app_state.repository.save(device)
    return device.to_dict(mask_sensitive=True)


@app.delete("/api/v1/devices/{device_id}", tags=["Devices"], status_code=204)
async def delete_device(device_id: int) -> None:
    """Delete a device by ID.

    Args:
        device_id: The device ID to delete.
    """
    if not app_state.repository:
        raise HTTPException(status_code=500, detail="Repository not initialized")

    device = app_state.repository.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    app_state.repository.delete(device_id)


# Scan endpoints
@app.post("/api/v1/scans", tags=["Scans"], status_code=202)
async def start_scan(
    scan_request: ScanRequest, background_tasks: BackgroundTasks
) -> ScanStatus:
    """Start a new network scan.

    Args:
        scan_request: Scan configuration.
        background_tasks: FastAPI background tasks handler.

    Returns:
        Scan job status.
    """
    job_id = str(uuid4())

    # Initialize scan job
    scan_jobs[job_id] = {
        "status": "pending",
        "network": scan_request.network,
        "total_devices": 0,
        "scanned_devices": 0,
        "started_at": None,
        "completed_at": None,
        "error": None,
        "devices": [],
    }

    # Start scan in background
    background_tasks.add_task(
        run_scan,
        job_id,
        scan_request.network,
        scan_request.enable_os_detection,
        scan_request.max_concurrent,
        scan_request.rate_limit,
    )

    return ScanStatus(
        job_id=job_id,
        status="pending",
        network=scan_request.network,
        total_devices=0,
        scanned_devices=0,
        started_at=None,
        completed_at=None,
        error=None,
    )


async def run_scan(
    job_id: str,
    network: str,
    enable_os_detection: bool,
    max_concurrent: int,
    rate_limit: float,
) -> None:
    """Run a network scan in the background.

    Args:
        job_id: Unique job identifier.
        network: Network CIDR to scan.
        enable_os_detection: Enable OS fingerprinting.
        max_concurrent: Maximum concurrent scans.
        rate_limit: Scans per second.
    """
    job = scan_jobs[job_id]
    job["status"] = "running"
    job["started_at"] = datetime.now(timezone.utc).isoformat()

    try:
        # Create rate limiter
        rate_limiter = RateLimiter(
            max_concurrent=max_concurrent,
            tokens_per_second=rate_limit,
        )

        # Create scanner with rate limiting
        scanner = NmapDeviceScanner(
            rate_limiter=rate_limiter,
            enable_os_detection=enable_os_detection,
        )

        # Create discovery service
        discovery = DeviceDiscoveryService(
            scanner=scanner,
            repository=app_state.repository,
        )

        # Run discovery
        devices = await discovery.discover_network(network)

        job["total_devices"] = len(devices)
        job["scanned_devices"] = len(devices)
        job["devices"] = [d.to_dict(mask_sensitive=True) for d in devices]
        job["status"] = "completed"
        job["completed_at"] = datetime.now(timezone.utc).isoformat()

    except Exception as e:
        logger.error("Scan job %s failed: %s", job_id, e)
        job["status"] = "failed"
        job["error"] = str(e)
        job["completed_at"] = datetime.now(timezone.utc).isoformat()


@app.get("/api/v1/scans/{job_id}", tags=["Scans"])
async def get_scan_status(job_id: str) -> ScanStatus:
    """Get scan job status.

    Args:
        job_id: The scan job ID.

    Returns:
        Scan job status.
    """
    if job_id not in scan_jobs:
        raise HTTPException(status_code=404, detail="Scan job not found")

    job = scan_jobs[job_id]
    return ScanStatus(
        job_id=job_id,
        status=job["status"],
        network=job["network"],
        total_devices=job["total_devices"],
        scanned_devices=job["scanned_devices"],
        started_at=job["started_at"],
        completed_at=job["completed_at"],
        error=job["error"],
    )


@app.get("/api/v1/scans/{job_id}/devices", tags=["Scans"])
async def get_scan_devices(job_id: str) -> list[dict[str, Any]]:
    """Get devices discovered in a scan job.

    Args:
        job_id: The scan job ID.

    Returns:
        List of discovered devices.
    """
    if job_id not in scan_jobs:
        raise HTTPException(status_code=404, detail="Scan job not found")

    return scan_jobs[job_id].get("devices", [])


@app.delete("/api/v1/scans/{job_id}", tags=["Scans"], status_code=204)
async def delete_scan_job(job_id: str) -> None:
    """Delete a scan job.

    Args:
        job_id: The scan job ID to delete.
    """
    if job_id not in scan_jobs:
        raise HTTPException(status_code=404, detail="Scan job not found")

    del scan_jobs[job_id]


# Report endpoints
@app.post("/api/v1/reports", tags=["Reports"])
async def generate_report(report_request: ReportRequest) -> dict[str, Any]:
    """Generate a report of all devices.

    Args:
        report_request: Report configuration.

    Returns:
        Report metadata and download URL.
    """
    if not app_state.repository or not app_state.report_generator:
        raise HTTPException(status_code=500, detail="Services not initialized")

    devices = app_state.repository.get_all()

    if not devices:
        raise HTTPException(status_code=404, detail="No devices to report")

    try:
        # Generate report
        report_path = app_state.report_generator.generate_report(
            devices, report_request.format
        )

        return {
            "format": report_request.format,
            "device_count": len(devices),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "download_path": f"/api/v1/reports/download/{Path(report_path).name}",
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None
    except Exception as e:
        logger.error("Report generation failed: %s", e)
        raise HTTPException(
            status_code=500, detail="Report generation failed"
        ) from None


@app.get("/api/v1/reports/formats", tags=["Reports"])
async def get_report_formats() -> list[str]:
    """Get available report formats.

    Returns:
        List of supported report formats.
    """
    if not app_state.report_generator:
        return ["json", "csv", "xlsx", "html"]

    return app_state.report_generator.supported_formats


# Statistics endpoint
@app.get("/api/v1/statistics", tags=["Statistics"])
async def get_statistics() -> dict[str, Any]:
    """Get discovery statistics.

    Returns:
        Statistics summary.
    """
    if not app_state.repository:
        raise HTTPException(status_code=500, detail="Repository not initialized")

    devices = app_state.repository.get_all()

    # Calculate statistics
    total = len(devices)
    alive = sum(1 for d in devices if d.alive)
    with_ssh = sum(1 for d in devices if d.ssh)
    with_snmp = sum(1 for d in devices if d.snmp)
    with_mysql = sum(1 for d in devices if d.mysql)
    with_http = sum(1 for d in devices if d.http)
    with_https = sum(1 for d in devices if d.https)
    scanned = sum(1 for d in devices if d.scanned)
    with_errors = sum(1 for d in devices if d.errors)

    return {
        "total_devices": total,
        "alive_devices": alive,
        "scanned_devices": scanned,
        "services": {
            "ssh": with_ssh,
            "snmp": with_snmp,
            "mysql": with_mysql,
            "http": with_http,
            "https": with_https,
        },
        "devices_with_errors": with_errors,
        "scan_jobs_active": sum(
            1 for j in scan_jobs.values() if j["status"] == "running"
        ),
        "scan_jobs_total": len(scan_jobs),
    }


def create_app(
    repository_path: Path | None = None,
    template_dir: Path | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        repository_path: Path to JSON repository file.
        template_dir: Path to HTML templates directory.

    Returns:
        Configured FastAPI application.
    """
    app_state.initialize(repository_path, template_dir)
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
