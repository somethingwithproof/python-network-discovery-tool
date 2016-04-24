import subprocess
from snimpy.manager import Manager as M
from snimpy.manager import load
import paramiko
import MySQLdb
import socket
from multiprocessing import Pool
from enum import Enum

USER = 'zenossmon'
KEY_FILE = '/home/thomas/.ssh/id_rsa.pub'


class ScanTypes(Enum):
    ping = 1
    snmp = 2
    ssh = 3
    mysql = 4

class DeviceScanResult:
    def __init__(self, device_id, scan_type, errors):
        self.device_id = device_id
        self.scan_type = scan_type
        self.errors = errors


class PingScanResult(DeviceScanResult):
    def __init__(self, device_id, output, errors):
        super().__init__(device_id, ScanTypes.ping, errors)
        self.output = output


class SSHScanResult(DeviceScanResult):
    def __init__(self, device_id, uname, errors):
        super().__init__(device_id, ScanTypes.ssh, errors)
        self.uname = uname


def test_ping(device):
    errors = []
    try:
        output = subprocess.check_output(
            "ping -c 1 -w 20 {}".format(device.host), shell=True)
    except subprocess.CalledProcessError as e:
        errors.append("(ping) " + str(e))
    finally:
        return PingScanResult(device.id, output, errors)


def test_ssh(device):
    errors = []
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(KEY_FILE)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(device.host, username=USER, timeout=3)
        _, stdout, _ = ssh.exec_command('uname -a')
        uname = stdout.read()
    except paramiko.AuthenticationException as e:
        errors.append("(ssh) " + str(e))
    except paramiko.SSHException as e:
        errors.append("(ssh) " + str(e))
    except socket.error as e:
        errors.append("(ssh) " + str(e))
    finally:
        return SSHScanResult(device.id, uname, errors)


class Device:

    def __init__(self, id, host, ip, snmp_group,
                 alive=False, snmp=False, ssh=False, errors="", mysql=False,
                 mysql_user='', mysql_password='', uname="", scanned=False):
        self.id = id
        self.host = host
        self.ip = ip
        if snmp_group != "":
            self.snmp_group = snmp_group
        else:
            self.snmp_group = "public"
        self.alive = alive == 1
        self.snmp = snmp == 1
        self.ssh = ssh == 1
        self.errors = errors
        self.mysql = mysql == 1
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.uname = uname
        self.scanned = scanned

    def scan(self, lock=None):
        self.is_alive(lock)
        self.has_snmp(lock)
        self.has_ssh(lock)
        if self.mysql_user != "" and self.mysql_user is not None:
            self.has_mysql(lock)
        self.scanned = True

    def has_error(self, msg):
        if self.errors == "" or self.errors is None:
            self.errors = msg
        else:
            self.errors = self.errors + ", " + msg

    def is_alive(self, lock=None):
        alive = False
        try:
            if lock is not None:
                lock.acquire()
            output = subprocess.check_output(
                "ping -c 1 -w 20 {}".format(self.host), shell=True)
            if lock is not None:
                lock.release()
            alive = True
        except subprocess.CalledProcessError as e:
            self.has_error("(ping) " + e.message)
            alive = False

        self.alive = alive

    def has_ssh(self, lock=None):
        result = False
        ssh = paramiko.SSHClient()
        ssh.load_host_keys(KEY_FILE)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if lock is not None:
                lock.acquire()
            ssh.connect(self.host, username=USER, timeout=3)
            stdin, stdout, stderr = ssh.exec_command('uname -a')
            self.uname = stdout.read()
            if lock is not None:
                lock.release()
            self.ssh = True
            result = True
        except paramiko.SSHException as e:
            self.has_error("(ssh) ", e.message)
        except paramiko.AuthenticationException as e:
            self.has_error("(ssh) " + e.message)
        except socket.error as e:
            self.has_error("(ssh) " + e.message)
        finally:
            self.ssh = result

    def has_snmp(self, lock=None):
        load("SNMPv2-MIB")
        self.snmp = False
        try:
            if lock is not None:
                lock.acquire()
            m = M(host=self.host, community=self.snmp_group,
                  version=2, timeout=2)
            if m.sysName is not None:
                self.snmp = True
            if lock is not None:
                lock.release()
        except Exception as e:
            self.has_error("(snmp) " + e.message)
            self.snmp = False

    def has_mysql(self, lock=None):
        try:
            if lock is not None:
                lock.acquire()
            db = MySQLdb.connect(
                self.host, self.mysql_user, self.mysql_password)
            cursor = db.cursor()
            cursor.execute("SELECT VERSION()")
            results = cursor.fetchone()
            if lock is not None:
                lock.release()
            # Check if anything at all is returned
            if results:
                self.mysql = True
            else:
                self.mysql = False
        except MySQLdb.Error as e:
            self.has_error("(mysql) " + e.message)
            self.mysql = False
        finally:
            db.close()

    def to_dict(self):
        device_dict = {
            "id":             self.id,
            "host":           self.host,
            "ip":             self.ip,
            "snmp_group":     self.snmp_group,
            "alive":          self.alive,
            "snmp":           self.snmp,
            "ssh":            self.ssh,
            "mysql_user":     self.mysql_user,
            "mysql_password": self.mysql_password,
            "uname":          self.uname,
            "scanned":        self.scanned
        }
        return device_dict

    def __repr__(self):
        return "{0} ({1})".format(self.host, self.ip)

    def __str__(self):
        return str(self.to_dict())
