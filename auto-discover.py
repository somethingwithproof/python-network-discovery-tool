import csv
import logging
import argparse
import socket
import time

import nmap
import paramiko
from snimpy.manager import Manager as SnimpyManager
from snimpy.manager import load

logger = logging.getLogger(__name__)


def read_hosts(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


class Device:
    def __init__(self, name, state, ssh, snmp):
        self.name = name
        self.state = state
        self.ssh = ssh
        self.snmp = snmp

    def to_dict(self):
        return {'name': self.name, 'state': self.state, 'ssh': self.ssh, 'snmp': self.snmp}

    def __repr__(self):
        return f"Device(name={self.name}, state={self.state}, ssh={self.ssh}, snmp={self.snmp})"

    def __str__(self):
        return self.name


class DeviceScanner:
    def __init__(self, hosts, port):
        self.hosts = hosts
        self.port = port

    def scan(self):
        devices = []
        for host in self.hosts:
            nm = nmap.PortScanner()
            nm.scan(host, str(self.port))
            state = nm[host].state()
            ssh_state = nm[host]['tcp'][22]['state'] if 'tcp' in nm[host] and 22 in nm[host]['tcp'] else None
            snmp_state = self._have_snmp(str(host))
            devices.append(Device(host, state, ssh_state, snmp_state))
        return devices

    def _have_snmp(self, host):
        try:
            load('SNMPv2-MIB')
            m = SnimpyManager(host=host, community='public', version=2)
            return 'open' if m.sysName is not None else 'closed'
        except Exception as e:
            logger.warning(f"SNMP check for host {host} failed: {e}")
            return 'closed'


class SshChecker:
    def __init__(self, user, key_file, retries=1, initial_wait=0, interval=0):
        self.user = user
        self.key_file = key_file
        self.retries = retries
        self.initial_wait = initial_wait
        self.interval = interval

    def check(self, device):
        if device.ssh != 'open':
            return False
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        time.sleep(self.initial_wait)
        for x in range(self.retries):
            try:
                ssh.connect(device.name, username=self.user, key_filename=self.key_file)
                return True
            except (paramiko.BadHostKeyException, paramiko.AuthenticationException,
                    paramiko.SSHException, socket.error) as e:
                logger.warning(f"SSH check for host {device.name} failed: {e}")
                time.sleep(self.interval)
            except Exception as e:
                logger.warning(f"SSH check for host {device.name} failed: {e}")
                time.sleep(self.interval)
        return False


class CsvWriter:
    def __init__(self, output_file):
        self.output_file = output_file

    def write_devices(self, devices):
        with open(self.output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['name', 'state', 'ssh', 'snmp'])
            for device in devices:
                writer.writerow([device['name'], device['state'], device['ssh'], device['snmp']])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Discover info of network devices.')
    parser.add_argument('inputfile', help='file with hosts to scan')
    parser.add_argument('outputfile', help='csv file to write devices info')

    args = parser.parse_args()

    hosts_to_scan = read_hosts(args.inputfile)

    nm = nmap.PortScanner()
    nm.scan(' '.join(hosts_to_scan), '22')

    devices = []
    for host in nm.all_hosts():
        state = nm[host].state()
        ssh = nm[host]['tcp'][22]['state']
        snmp = have_snmp(str(host))
        devices.append({'name': host, 'state': state, 'ssh': ssh, 'snmp': snmp})

    writer = CsvWriter(args.outputfile)
    writer.write_devices(devices)
