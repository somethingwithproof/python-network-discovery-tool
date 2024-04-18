import argparse
import csv
import logging
from pathlib import Path
import asyncio
import asyncssh
import nmap

# Setup logging
logger = logging.getLogger('network_scanner')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('network_scan.log', 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def read_hosts(filename):
    """Read host names from a file.
    
    Args:
        filename (Path): The path to the file containing hostnames.

    Returns:
        list: A list of host names.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

class Device:
    """Represents a network device with scanning results."""
    def __init__(self, name, state, ssh, snmp):
        self.name = name
        self.state = state
        self.ssh = ssh
        self.snmp = snmp

    def to_dict(self):
        """Convert device attributes to dictionary format for easy CSV writing."""
        return {'name': self.name, 'state': self.state, 'ssh': self.ssh, 'snmp': self.snmp}

class DeviceScanner:
    """Scans devices using nmap for SSH and SNMP availability."""
    def __init__(self, hosts):
        self.hosts = hosts
        self.nm = nmap.PortScanner()

    def scan(self):
        """Perform the scanning of assigned hosts.

        Returns:
            list: A list of Device instances with scanned results.
        """
        self.nm.scan(','.join(self.hosts), arguments='-p 22,161')
        return [Device(host, self.nm[host].state(),
                       self.nm[host]['tcp'][22]['state'] if 22 in self.nm[host]['tcp'] else 'closed',
                       'open' if 161 in self.nm[host]['tcp'] and self.nm[host]['tcp'][161]['state'] == 'open' else 'closed')
                for host in self.hosts]

async def check_ssh_async(device):
    """Asynchronously check SSH connectivity for a device.

    Args:
        device (Device): The device to check SSH connectivity.

    Returns:
        Device: The device with updated SSH status.
    """
    if device.ssh != 'open':
        return device
    try:
        async with asyncssh.connect(device.name) as conn:
            result = await conn.run('uname -a', check=True)
            device.ssh = result.stdout.strip()
    except asyncssh.Error as e:
        logger.error(f'SSH check failed for {device.name}: {str(e)}')
        device.ssh = 'closed'
    return device

class CsvWriter:
    """Writes devices information to a CSV file."""
    def __init__(self, output_file):
        self.output_file = output_file

    def write_devices(self, devices):
        """Write the list of devices to a CSV file.

        Args:
            devices (list): A list of Device objects to write to the CSV.
        """
        with open(self.output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'state', 'ssh', 'snmp'])
            writer.writeheader()
            for device in devices:
                writer.writerow(device.to_dict())

async def perform_ssh_checks(devices):
    """Perform asynchronous SSH checks on a list of devices.

    Args:
        devices (list): A list of Device objects to perform SSH checks.

    Returns:
        list: A list of devices with updated SSH status.
    """
    return await asyncio.gather(*[check_ssh_async(device) for device in devices if device.ssh == 'open'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network Device Discovery Tool')
    parser.add_argument('inputfile', type=Path, help='File with hosts to scan')
    parser.add_argument('outputfile', type=Path, help='CSV file to write devices info')
    args = parser.parse_args()

    hosts = read_hosts(args.inputfile)
    scanner = DeviceScanner(hosts)
    devices = scanner.scan()
   
