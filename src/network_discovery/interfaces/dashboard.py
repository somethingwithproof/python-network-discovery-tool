"""Material Design Web Dashboard for Network Discovery Tool.

This module provides a web-based dashboard using Google Material Design
components for visualizing network discovery results and managing scans.

Features:
- Real-time scan monitoring
- Device inventory display
- Statistics visualization
- Report generation
- Webhook configuration
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


if TYPE_CHECKING:
    from pathlib import Path

    from fastapi import FastAPI, Request


logger = logging.getLogger(__name__)

# Material Design Dashboard HTML Template
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Discovery Dashboard</title>

    <!-- Material Design Components -->
    <link href="https://unpkg.com/material-components-web@14.0.0/dist/material-components-web.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --mdc-theme-primary: #1976d2;
            --mdc-theme-secondary: #388e3c;
            --mdc-theme-surface: #ffffff;
            --mdc-theme-background: #fafafa;
            --mdc-theme-error: #d32f2f;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            font-family: 'Roboto', sans-serif;
            background-color: var(--mdc-theme-background);
        }

        .mdc-top-app-bar {
            background-color: var(--mdc-theme-primary);
        }

        .main-content {
            padding: 84px 24px 24px;
            max-width: 1400px;
            margin: 0 auto;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: var(--mdc-theme-surface);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }

        .stat-card .stat-value {
            font-size: 2.5rem;
            font-weight: 500;
            color: var(--mdc-theme-primary);
            margin-bottom: 8px;
        }

        .stat-card .stat-label {
            font-size: 0.875rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .card {
            background: var(--mdc-theme-surface);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 24px;
            overflow: hidden;
        }

        .card-header {
            padding: 16px 20px;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-header h2 {
            margin: 0;
            font-size: 1.25rem;
            font-weight: 500;
        }

        .card-content {
            padding: 20px;
        }

        .scan-form {
            display: grid;
            grid-template-columns: 1fr 1fr auto;
            gap: 16px;
            align-items: end;
        }

        @media (max-width: 768px) {
            .scan-form {
                grid-template-columns: 1fr;
            }
        }

        .mdc-text-field {
            width: 100%;
        }

        .mdc-data-table {
            width: 100%;
            border: none;
        }

        .mdc-data-table__header-cell {
            background-color: #f5f5f5;
        }

        .service-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            margin-right: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }

        .service-icon.active {
            background-color: #e8f5e9;
            color: #2e7d32;
        }

        .service-icon.inactive {
            background-color: #f5f5f5;
            color: #9e9e9e;
        }

        .status-chip {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.75rem;
            font-weight: 500;
        }

        .status-chip.alive {
            background-color: #e8f5e9;
            color: #2e7d32;
        }

        .status-chip.offline {
            background-color: #ffebee;
            color: #c62828;
        }

        .progress-container {
            display: none;
            align-items: center;
            gap: 16px;
            margin-top: 16px;
        }

        .progress-container.visible {
            display: flex;
        }

        .mdc-linear-progress {
            flex: 1;
        }

        .mdc-dialog__surface {
            min-width: 400px;
            max-width: 600px;
        }

        .device-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .device-details .detail-item {
            padding: 12px;
            background: #f5f5f5;
            border-radius: 4px;
        }

        .device-details .detail-label {
            font-size: 0.75rem;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 4px;
        }

        .device-details .detail-value {
            font-size: 1rem;
            color: #333;
            word-break: break-word;
        }

        .empty-state {
            text-align: center;
            padding: 48px 24px;
            color: #666;
        }

        .empty-state .material-icons {
            font-size: 64px;
            color: #e0e0e0;
            margin-bottom: 16px;
        }

        .action-buttons {
            display: flex;
            gap: 8px;
        }

        .mdc-snackbar {
            bottom: 24px;
        }

        .refresh-indicator {
            display: none;
            margin-left: 8px;
        }

        .refresh-indicator.visible {
            display: inline-block;
        }
    </style>
</head>
<body>
    <!-- Top App Bar -->
    <header class="mdc-top-app-bar mdc-top-app-bar--fixed">
        <div class="mdc-top-app-bar__row">
            <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
                <span class="material-icons mdc-top-app-bar__navigation-icon">device_hub</span>
                <span class="mdc-top-app-bar__title">Network Discovery</span>
            </section>
            <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-end">
                <button class="mdc-icon-button material-icons" id="refresh-btn" title="Refresh">
                    refresh
                </button>
                <div class="mdc-circular-progress mdc-circular-progress--indeterminate refresh-indicator" id="refresh-indicator" role="progressbar">
                    <div class="mdc-circular-progress__determinate-container">
                        <svg class="mdc-circular-progress__determinate-circle-graphic" viewBox="0 0 24 24">
                            <circle class="mdc-circular-progress__determinate-track" cx="12" cy="12" r="8.75" stroke-width="2.5"/>
                            <circle class="mdc-circular-progress__determinate-circle" cx="12" cy="12" r="8.75" stroke-dasharray="54.978" stroke-dashoffset="54.978" stroke-width="2.5"/>
                        </svg>
                    </div>
                </div>
                <button class="mdc-icon-button material-icons" id="export-btn" title="Export Report">
                    download
                </button>
                <button class="mdc-icon-button material-icons" id="settings-btn" title="Settings">
                    settings
                </button>
            </section>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        <!-- Statistics Cards -->
        <div class="stats-grid" id="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="stat-total">-</div>
                <div class="stat-label">Total Devices</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-alive">-</div>
                <div class="stat-label">Online</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-ssh">-</div>
                <div class="stat-label">SSH</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-http">-</div>
                <div class="stat-label">HTTP/HTTPS</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-snmp">-</div>
                <div class="stat-label">SNMP</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-mysql">-</div>
                <div class="stat-label">MySQL</div>
            </div>
        </div>

        <!-- Network Scan Card -->
        <div class="card">
            <div class="card-header">
                <h2>Network Scan</h2>
            </div>
            <div class="card-content">
                <form class="scan-form" id="scan-form">
                    <div class="mdc-text-field mdc-text-field--outlined">
                        <input type="text" id="network-input" class="mdc-text-field__input"
                               placeholder="192.168.1.0/24" required>
                        <div class="mdc-notched-outline">
                            <div class="mdc-notched-outline__leading"></div>
                            <div class="mdc-notched-outline__notch">
                                <label class="mdc-floating-label" for="network-input">Network CIDR</label>
                            </div>
                            <div class="mdc-notched-outline__trailing"></div>
                        </div>
                    </div>
                    <div class="mdc-text-field mdc-text-field--outlined">
                        <input type="number" id="rate-input" class="mdc-text-field__input"
                               value="10" min="1" max="100">
                        <div class="mdc-notched-outline">
                            <div class="mdc-notched-outline__leading"></div>
                            <div class="mdc-notched-outline__notch">
                                <label class="mdc-floating-label" for="rate-input">Max Concurrent</label>
                            </div>
                            <div class="mdc-notched-outline__trailing"></div>
                        </div>
                    </div>
                    <button type="submit" class="mdc-button mdc-button--raised" id="scan-btn">
                        <span class="mdc-button__ripple"></span>
                        <span class="material-icons mdc-button__icon">search</span>
                        <span class="mdc-button__label">Start Scan</span>
                    </button>
                </form>
                <div class="progress-container" id="scan-progress">
                    <div role="progressbar" class="mdc-linear-progress" aria-valuemin="0" aria-valuemax="1">
                        <div class="mdc-linear-progress__buffer">
                            <div class="mdc-linear-progress__buffer-bar"></div>
                            <div class="mdc-linear-progress__buffer-dots"></div>
                        </div>
                        <div class="mdc-linear-progress__bar mdc-linear-progress__primary-bar">
                            <span class="mdc-linear-progress__bar-inner"></span>
                        </div>
                        <div class="mdc-linear-progress__bar mdc-linear-progress__secondary-bar">
                            <span class="mdc-linear-progress__bar-inner"></span>
                        </div>
                    </div>
                    <span id="scan-status">Scanning...</span>
                </div>
            </div>
        </div>

        <!-- Devices Table Card -->
        <div class="card">
            <div class="card-header">
                <h2>Discovered Devices</h2>
                <div class="action-buttons">
                    <button class="mdc-button mdc-button--outlined" id="filter-online-btn">
                        <span class="mdc-button__ripple"></span>
                        <span class="mdc-button__label">Online Only</span>
                    </button>
                </div>
            </div>
            <div class="card-content" id="devices-container">
                <div class="mdc-data-table">
                    <div class="mdc-data-table__table-container">
                        <table class="mdc-data-table__table" id="devices-table">
                            <thead>
                                <tr class="mdc-data-table__header-row">
                                    <th class="mdc-data-table__header-cell">Host</th>
                                    <th class="mdc-data-table__header-cell">IP Address</th>
                                    <th class="mdc-data-table__header-cell">Status</th>
                                    <th class="mdc-data-table__header-cell">Services</th>
                                    <th class="mdc-data-table__header-cell">OS</th>
                                    <th class="mdc-data-table__header-cell">Actions</th>
                                </tr>
                            </thead>
                            <tbody class="mdc-data-table__content" id="devices-tbody">
                                <!-- Device rows will be inserted here -->
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="empty-state" id="empty-state">
                    <span class="material-icons">devices_other</span>
                    <p>No devices discovered yet. Start a network scan to find devices.</p>
                </div>
            </div>
        </div>
    </main>

    <!-- Device Details Dialog -->
    <div class="mdc-dialog" id="device-dialog">
        <div class="mdc-dialog__container">
            <div class="mdc-dialog__surface">
                <h2 class="mdc-dialog__title" id="dialog-title">Device Details</h2>
                <div class="mdc-dialog__content" id="dialog-content">
                    <div class="device-details" id="device-details">
                        <!-- Device details will be inserted here -->
                    </div>
                </div>
                <div class="mdc-dialog__actions">
                    <button type="button" class="mdc-button mdc-dialog__button" data-mdc-dialog-action="close">
                        <span class="mdc-button__ripple"></span>
                        <span class="mdc-button__label">Close</span>
                    </button>
                    <button type="button" class="mdc-button mdc-button--raised mdc-dialog__button" id="rescan-device-btn">
                        <span class="mdc-button__ripple"></span>
                        <span class="mdc-button__label">Rescan</span>
                    </button>
                </div>
            </div>
        </div>
        <div class="mdc-dialog__scrim"></div>
    </div>

    <!-- Export Dialog -->
    <div class="mdc-dialog" id="export-dialog">
        <div class="mdc-dialog__container">
            <div class="mdc-dialog__surface">
                <h2 class="mdc-dialog__title">Export Report</h2>
                <div class="mdc-dialog__content">
                    <p>Select the export format:</p>
                    <div class="mdc-form-field">
                        <div class="mdc-radio">
                            <input class="mdc-radio__native-control" type="radio" name="export-format" value="json" id="format-json" checked>
                            <div class="mdc-radio__background">
                                <div class="mdc-radio__outer-circle"></div>
                                <div class="mdc-radio__inner-circle"></div>
                            </div>
                            <div class="mdc-radio__ripple"></div>
                        </div>
                        <label for="format-json">JSON</label>
                    </div>
                    <div class="mdc-form-field">
                        <div class="mdc-radio">
                            <input class="mdc-radio__native-control" type="radio" name="export-format" value="csv" id="format-csv">
                            <div class="mdc-radio__background">
                                <div class="mdc-radio__outer-circle"></div>
                                <div class="mdc-radio__inner-circle"></div>
                            </div>
                            <div class="mdc-radio__ripple"></div>
                        </div>
                        <label for="format-csv">CSV</label>
                    </div>
                    <div class="mdc-form-field">
                        <div class="mdc-radio">
                            <input class="mdc-radio__native-control" type="radio" name="export-format" value="xlsx" id="format-xlsx">
                            <div class="mdc-radio__background">
                                <div class="mdc-radio__outer-circle"></div>
                                <div class="mdc-radio__inner-circle"></div>
                            </div>
                            <div class="mdc-radio__ripple"></div>
                        </div>
                        <label for="format-xlsx">Excel (XLSX)</label>
                    </div>
                    <div class="mdc-form-field">
                        <div class="mdc-radio">
                            <input class="mdc-radio__native-control" type="radio" name="export-format" value="html" id="format-html">
                            <div class="mdc-radio__background">
                                <div class="mdc-radio__outer-circle"></div>
                                <div class="mdc-radio__inner-circle"></div>
                            </div>
                            <div class="mdc-radio__ripple"></div>
                        </div>
                        <label for="format-html">HTML</label>
                    </div>
                    <br>
                    <div class="mdc-form-field">
                        <div class="mdc-checkbox">
                            <input type="checkbox" class="mdc-checkbox__native-control" id="mask-sensitive" checked/>
                            <div class="mdc-checkbox__background">
                                <svg class="mdc-checkbox__checkmark" viewBox="0 0 24 24">
                                    <path class="mdc-checkbox__checkmark-path" fill="none" d="M1.73,12.91 8.1,19.28 22.79,4.59"/>
                                </svg>
                                <div class="mdc-checkbox__mixedmark"></div>
                            </div>
                            <div class="mdc-checkbox__ripple"></div>
                        </div>
                        <label for="mask-sensitive">Mask sensitive data (passwords)</label>
                    </div>
                </div>
                <div class="mdc-dialog__actions">
                    <button type="button" class="mdc-button mdc-dialog__button" data-mdc-dialog-action="cancel">
                        <span class="mdc-button__ripple"></span>
                        <span class="mdc-button__label">Cancel</span>
                    </button>
                    <button type="button" class="mdc-button mdc-button--raised mdc-dialog__button" id="export-confirm-btn">
                        <span class="mdc-button__ripple"></span>
                        <span class="mdc-button__label">Export</span>
                    </button>
                </div>
            </div>
        </div>
        <div class="mdc-dialog__scrim"></div>
    </div>

    <!-- Snackbar for notifications -->
    <div class="mdc-snackbar" id="snackbar">
        <div class="mdc-snackbar__surface">
            <div class="mdc-snackbar__label" id="snackbar-label"></div>
            <div class="mdc-snackbar__actions">
                <button type="button" class="mdc-icon-button mdc-snackbar__dismiss material-icons">close</button>
            </div>
        </div>
    </div>

    <!-- Material Design Components JS -->
    <script src="https://unpkg.com/material-components-web@14.0.0/dist/material-components-web.min.js"></script>

    <script>
        // Initialize Material Design Components
        mdc.autoInit();

        // Initialize specific components
        const textFields = document.querySelectorAll('.mdc-text-field');
        textFields.forEach(tf => new mdc.textField.MDCTextField(tf));

        const deviceDialog = new mdc.dialog.MDCDialog(document.getElementById('device-dialog'));
        const exportDialog = new mdc.dialog.MDCDialog(document.getElementById('export-dialog'));
        const snackbar = new mdc.snackbar.MDCSnackbar(document.getElementById('snackbar'));

        // API base URL
        const API_BASE = '/api/v1';

        // State
        let devices = [];
        let currentDevice = null;
        let filterOnlineOnly = false;
        let currentScanJobId = null;

        // Utility function to create text node safely
        function safeText(text) {
            return document.createTextNode(text || '');
        }

        // Clear element content safely
        function clearElement(element) {
            while (element.firstChild) {
                element.removeChild(element.firstChild);
            }
        }

        // Show snackbar notification
        function showNotification(message) {
            const label = document.getElementById('snackbar-label');
            clearElement(label);
            label.appendChild(safeText(message));
            snackbar.open();
        }

        // Fetch statistics
        async function fetchStatistics() {
            try {
                const response = await fetch(`${API_BASE}/statistics`);
                if (response.ok) {
                    const stats = await response.json();
                    document.getElementById('stat-total').textContent = stats.total_devices || 0;
                    document.getElementById('stat-alive').textContent = stats.alive_devices || 0;
                    document.getElementById('stat-ssh').textContent = stats.services?.ssh || 0;
                    document.getElementById('stat-http').textContent =
                        (stats.services?.http || 0) + (stats.services?.https || 0);
                    document.getElementById('stat-snmp').textContent = stats.services?.snmp || 0;
                    document.getElementById('stat-mysql').textContent = stats.services?.mysql || 0;
                }
            } catch (error) {
                console.error('Failed to fetch statistics:', error);
            }
        }

        // Fetch devices
        async function fetchDevices() {
            try {
                const indicator = document.getElementById('refresh-indicator');
                indicator.classList.add('visible');

                const response = await fetch(`${API_BASE}/devices`);
                if (response.ok) {
                    devices = await response.json();
                    renderDevices();
                }

                indicator.classList.remove('visible');
            } catch (error) {
                console.error('Failed to fetch devices:', error);
                showNotification('Failed to load devices');
                document.getElementById('refresh-indicator').classList.remove('visible');
            }
        }

        // Create service icon element
        function createServiceIcon(name, active) {
            const span = document.createElement('span');
            span.className = 'service-icon ' + (active ? 'active' : 'inactive');
            span.title = name;
            span.textContent = name.substring(0, 2).toUpperCase();
            return span;
        }

        // Create status chip element
        function createStatusChip(alive) {
            const span = document.createElement('span');
            span.className = 'status-chip ' + (alive ? 'alive' : 'offline');
            span.textContent = alive ? 'Online' : 'Offline';
            return span;
        }

        // Create action button
        function createActionButton(deviceId) {
            const button = document.createElement('button');
            button.className = 'mdc-icon-button material-icons';
            button.title = 'View Details';
            button.textContent = 'visibility';
            button.addEventListener('click', () => showDeviceDetails(deviceId));
            return button;
        }

        // Render devices table
        function renderDevices() {
            const tbody = document.getElementById('devices-tbody');
            const emptyState = document.getElementById('empty-state');

            clearElement(tbody);

            let filteredDevices = devices;
            if (filterOnlineOnly) {
                filteredDevices = devices.filter(d => d.alive);
            }

            if (filteredDevices.length === 0) {
                emptyState.style.display = 'block';
                return;
            }

            emptyState.style.display = 'none';

            filteredDevices.forEach(device => {
                const row = document.createElement('tr');
                row.className = 'mdc-data-table__row';

                // Host cell
                const hostCell = document.createElement('td');
                hostCell.className = 'mdc-data-table__cell';
                hostCell.textContent = device.host || '-';
                row.appendChild(hostCell);

                // IP cell
                const ipCell = document.createElement('td');
                ipCell.className = 'mdc-data-table__cell';
                ipCell.textContent = device.ip || '-';
                row.appendChild(ipCell);

                // Status cell
                const statusCell = document.createElement('td');
                statusCell.className = 'mdc-data-table__cell';
                statusCell.appendChild(createStatusChip(device.alive));
                row.appendChild(statusCell);

                // Services cell
                const servicesCell = document.createElement('td');
                servicesCell.className = 'mdc-data-table__cell';
                servicesCell.appendChild(createServiceIcon('SSH', device.ssh));
                servicesCell.appendChild(createServiceIcon('HTTP', device.http));
                servicesCell.appendChild(createServiceIcon('HTTPS', device.https));
                servicesCell.appendChild(createServiceIcon('SNMP', device.snmp));
                servicesCell.appendChild(createServiceIcon('MySQL', device.mysql));
                row.appendChild(servicesCell);

                // OS cell
                const osCell = document.createElement('td');
                osCell.className = 'mdc-data-table__cell';
                osCell.textContent = device.os_fingerprint
                    ? (device.os_fingerprint.substring(0, 30) + (device.os_fingerprint.length > 30 ? '...' : ''))
                    : '-';
                osCell.title = device.os_fingerprint || '';
                row.appendChild(osCell);

                // Actions cell
                const actionsCell = document.createElement('td');
                actionsCell.className = 'mdc-data-table__cell';
                actionsCell.appendChild(createActionButton(device.id));
                row.appendChild(actionsCell);

                tbody.appendChild(row);
            });
        }

        // Create detail item element
        function createDetailItem(label, value) {
            const item = document.createElement('div');
            item.className = 'detail-item';

            const labelDiv = document.createElement('div');
            labelDiv.className = 'detail-label';
            labelDiv.textContent = label;
            item.appendChild(labelDiv);

            const valueDiv = document.createElement('div');
            valueDiv.className = 'detail-value';
            valueDiv.textContent = value || '-';
            item.appendChild(valueDiv);

            return item;
        }

        // Show device details dialog
        async function showDeviceDetails(deviceId) {
            try {
                const response = await fetch(`${API_BASE}/devices/${deviceId}`);
                if (response.ok) {
                    currentDevice = await response.json();

                    const title = document.getElementById('dialog-title');
                    title.textContent = 'Device: ' + (currentDevice.host || currentDevice.ip);

                    const detailsContainer = document.getElementById('device-details');
                    clearElement(detailsContainer);

                    detailsContainer.appendChild(createDetailItem('Hostname', currentDevice.host));
                    detailsContainer.appendChild(createDetailItem('IP Address', currentDevice.ip));
                    detailsContainer.appendChild(createDetailItem('Status', currentDevice.alive ? 'Online' : 'Offline'));
                    detailsContainer.appendChild(createDetailItem('SNMP Community', currentDevice.snmp_group));
                    detailsContainer.appendChild(createDetailItem('SNMP Version', 'v' + currentDevice.snmp_version));
                    detailsContainer.appendChild(createDetailItem('OS Fingerprint', currentDevice.os_fingerprint));
                    detailsContainer.appendChild(createDetailItem('Server Headers', currentDevice.server_headers));
                    detailsContainer.appendChild(createDetailItem('SSL Info', currentDevice.ssl_info));
                    detailsContainer.appendChild(createDetailItem('Uname', currentDevice.uname));

                    const errorsText = currentDevice.errors && currentDevice.errors.length > 0
                        ? currentDevice.errors.join(', ')
                        : 'None';
                    detailsContainer.appendChild(createDetailItem('Errors', errorsText));

                    deviceDialog.open();
                } else {
                    showNotification('Device not found');
                }
            } catch (error) {
                console.error('Failed to fetch device details:', error);
                showNotification('Failed to load device details');
            }
        }

        // Start network scan
        async function startScan(network, maxConcurrent) {
            try {
                const response = await fetch(`${API_BASE}/scans`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        network: network,
                        max_concurrent: maxConcurrent,
                        enable_os_detection: true,
                        rate_limit: 5.0
                    })
                });

                if (response.ok) {
                    const result = await response.json();
                    currentScanJobId = result.job_id;
                    showNotification('Scan started');

                    // Show progress
                    document.getElementById('scan-progress').classList.add('visible');
                    document.getElementById('scan-btn').disabled = true;

                    // Poll for status
                    pollScanStatus();
                } else {
                    showNotification('Failed to start scan');
                }
            } catch (error) {
                console.error('Failed to start scan:', error);
                showNotification('Failed to start scan');
            }
        }

        // Poll scan status
        async function pollScanStatus() {
            if (!currentScanJobId) return;

            try {
                const response = await fetch(`${API_BASE}/scans/${currentScanJobId}`);
                if (response.ok) {
                    const status = await response.json();

                    document.getElementById('scan-status').textContent =
                        status.status + ' (' + status.scanned_devices + '/' + status.total_devices + ')';

                    if (status.status === 'completed') {
                        document.getElementById('scan-progress').classList.remove('visible');
                        document.getElementById('scan-btn').disabled = false;
                        showNotification('Scan completed: ' + status.scanned_devices + ' devices found');
                        currentScanJobId = null;

                        // Refresh data
                        fetchDevices();
                        fetchStatistics();
                    } else if (status.status === 'failed') {
                        document.getElementById('scan-progress').classList.remove('visible');
                        document.getElementById('scan-btn').disabled = false;
                        showNotification('Scan failed: ' + (status.error || 'Unknown error'));
                        currentScanJobId = null;
                    } else {
                        // Still running, poll again
                        setTimeout(pollScanStatus, 2000);
                    }
                }
            } catch (error) {
                console.error('Failed to poll scan status:', error);
            }
        }

        // Export report
        async function exportReport(format, maskSensitive) {
            try {
                const response = await fetch(`${API_BASE}/reports`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        format: format,
                        mask_sensitive: maskSensitive
                    })
                });

                if (response.ok) {
                    const result = await response.json();
                    showNotification('Report generated: ' + result.device_count + ' devices');

                    // Open download link if available
                    if (result.download_path) {
                        window.open(result.download_path, '_blank');
                    }
                } else {
                    const error = await response.json();
                    showNotification('Export failed: ' + (error.detail || 'Unknown error'));
                }
            } catch (error) {
                console.error('Failed to export report:', error);
                showNotification('Failed to export report');
            }
        }

        // Event listeners
        document.getElementById('scan-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const network = document.getElementById('network-input').value;
            const maxConcurrent = parseInt(document.getElementById('rate-input').value) || 10;
            startScan(network, maxConcurrent);
        });

        document.getElementById('refresh-btn').addEventListener('click', () => {
            fetchDevices();
            fetchStatistics();
        });

        document.getElementById('export-btn').addEventListener('click', () => {
            exportDialog.open();
        });

        document.getElementById('export-confirm-btn').addEventListener('click', () => {
            const format = document.querySelector('input[name="export-format"]:checked').value;
            const maskSensitive = document.getElementById('mask-sensitive').checked;
            exportReport(format, maskSensitive);
            exportDialog.close();
        });

        document.getElementById('filter-online-btn').addEventListener('click', () => {
            filterOnlineOnly = !filterOnlineOnly;
            const btn = document.getElementById('filter-online-btn');
            if (filterOnlineOnly) {
                btn.classList.add('mdc-button--raised');
                btn.classList.remove('mdc-button--outlined');
            } else {
                btn.classList.remove('mdc-button--raised');
                btn.classList.add('mdc-button--outlined');
            }
            renderDevices();
        });

        // Initial data load
        fetchStatistics();
        fetchDevices();

        // Auto-refresh every 30 seconds
        setInterval(() => {
            fetchStatistics();
            if (!currentScanJobId) {
                fetchDevices();
            }
        }, 30000);
    </script>
</body>
</html>
"""


def setup_dashboard(app: FastAPI) -> None:
    """Set up the Material Design dashboard routes.

    Args:
        app: The FastAPI application instance.
    """

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def dashboard_home(_request: Request) -> HTMLResponse:
        """Serve the main dashboard page.

        Args:
            _request: The incoming request (unused, required by FastAPI).

        Returns:
            HTML response with the dashboard.
        """
        return HTMLResponse(content=DASHBOARD_HTML)

    @app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
    async def dashboard_page(_request: Request) -> HTMLResponse:
        """Serve the dashboard page (alias).

        Args:
            _request: The incoming request (unused, required by FastAPI).

        Returns:
            HTML response with the dashboard.
        """
        return HTMLResponse(content=DASHBOARD_HTML)

    logger.info("Material Design dashboard routes configured")


def create_dashboard_app(
    static_dir: Path | None = None,
) -> FastAPI:
    """Create a standalone dashboard application.

    Args:
        static_dir: Optional directory for static files.

    Returns:
        Configured FastAPI application with dashboard.
    """
    from network_discovery.interfaces.api import app as api_app  # noqa: PLC0415

    # Set up dashboard routes
    setup_dashboard(api_app)

    # Mount static files if directory provided
    if static_dir and static_dir.exists():
        api_app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    return api_app


if __name__ == "__main__":
    import uvicorn

    app = create_dashboard_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
