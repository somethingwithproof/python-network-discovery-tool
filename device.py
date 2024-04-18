import json
import os
import logging
from typing import Optional, List, Any
from twisted.internet import defer, task
from twisted.python import log as twisted_log
from snimpy.manager import Manager as M, load
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException
import MySQLdb

# Setup logging
logger = logging.getLogger(__name__)

# Environment variables
USER = os.getenv('SSH_USER', 'zenossmon')
KEY_FILE = os.getenv('SSH_KEY_FILE', '/home/efren/.ssh/id_rsa.pub')
MYSQL_USER = os.getenv('MYSQL_USER', '')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')


class Device:
    """Represents a network device and provides methods to scan and check its various services."""

    def __init__(self, id: int, host: str, ip: str, snmp_group: str = "public", alive: bool = False,
                 snmp: bool = False, ssh: bool = False, mysql: bool = False, mysql_user: str = MYSQL_USER,
                 mysql_password: str = MYSQL_PASSWORD, uname: str = "", errors: Optional[List[str]] = None,
                 scanned: bool = False):
        self.id = id
        self.host = host
        self.ip = ip
        self.snmp_group = snmp_group
        self.alive = alive
        self.snmp = snmp
        self.ssh = ssh
        self.errors = errors if errors is not None else []
        self.mysql = mysql
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.uname = uname
        self.scanned = scanned

    def record(self, redis: Optional[Any] = None) -> None:
        """Records the device status in Redis."""
        if redis:
            redis.set(self.key(), self.to_json())

    @defer.inlineCallbacks
    def scan(self, redis: Optional[Any] = None) -> defer.Deferred:
        """Performs a scan to check the status of the device."""
        try:
            yield self.is_alive()
            self.record(redis)

            checks = [self.check_snmp(), self.check_ssh()]
            if self.mysql_user:
                checks.append(self.check_mysql())

            yield task.gatherResults(checks)

            if not self.alive:
                self.reset_services()
                self.add_error("(alive) Host is down")

            self.record(redis)
            self.scanned = True
        except Exception as e:
            self.add_error(f"(scan) Exception: {e}")

    def add_error(self, msg: str) -> None:
        """Adds an error message to the device's error log."""
        self.errors.append(msg)
        logger.error(msg)

    @defer.inlineCallbacks
    def is_alive(self) -> defer.Deferred:
        """Checks if the device is alive using an Nmap ping scan."""
        self.alive = False
        nmproc = NmapProcess(str(self.ip), '-sn')
        rc = nmproc.run()
        if rc != 0:
            self.add_error(f"(alive) {nmproc.stderr}")
        else:
            try:
                nmap_report = NmapParser.parse(nmproc.stdout)
                self.alive = (nmap_report.hosts[0].status == 'up')
            except NmapParserException as e:
                self.add_error(f"(alive) NmapParserException: {e}")

    @defer.inlineCallbacks
    def is_port_open(self, port: int) -> defer.Deferred:
        """Checks if a specific port on the device is open."""
        nmproc = NmapProcess(str(self.ip), f'-p {port}')
        rc = nmproc.run()
        if rc != 0:
            self.add_error(f"nmap scan failed: {nmproc.stderr}")
            defer.returnValue(False)
        else:
            try:
                nmap_report = NmapParser.parse(nmproc.stdout)
                if nmap_report.hosts[0].status == 'up':
                    defer.returnValue(nmap_report.hosts[0].services[0].state == 'open')
                else:
                    defer.returnValue(False)
            except NmapParserException as e:
                self.add_error(f"NmapParserException: {e}")
                defer.returnValue(False)

    @defer.inlineCallbacks
    def check_ssh(self) -> defer.Deferred:
        """Checks if SSH is available on the device."""
        self.ssh = False
        self.uname = "unknown"
        port_open = yield self.is_port_open(22)
        if not port_open:
            self.add_error("(ssh) Port closed")
            return

        try:
            result = yield SSHHelper.connect_and_run(self.host, USER, 'uname -a')
            self.uname = result.strip()
            self.ssh = True
        except (AuthenticationException, SSHException) as e:
            self.add_error(f"(ssh) {str(e)}")
        except Exception as e:
            self.add_error(f"(ssh) {str(e)}")

    @defer.inlineCallbacks
    def check_snmp(self) -> defer.Deferred:
        """Checks if SNMP is available on the device."""
        self.snmp = False
        try:
            result = yield SNMPAgent.check_snmp(self.host, self.snmp_group)
            self.snmp = result
        except Exception as e:
            self.add_error(f"(snmp) {str(e)}")

    @defer.inlineCallbacks
    def check_mysql(self) -> defer.Deferred:
        """Checks if MySQL is available on the device."""
        self.mysql = False
        port_open = yield self.is_port_open(3306)
        if not port_open:
            self.add_error("(mysql) Port closed")
            return
        try:
            result = yield MySQLHelper.check_mysql(self.host, self.mysql_user, self.mysql_password)
            self.mysql = result
        except MySQLdb.OperationalError as e:
            self.add_error(f"(mysql) {str(e)}")

    def reset_services(self) -> None:
        """Resets the statuses of all services."""
        self.ssh = False
        self.snmp = False
        self.mysql = False
        self.uname = "unknown"

    def key(self) -> str:
        """Returns a unique key for the device."""
        return f"device:{self.id}"

    def to_json(self) -> str:
        """Serializes the device to a JSON string."""
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        """Converts the device attributes to a dictionary."""
        return {
            "id": self.id,
            "host": self.host,
            "ip": self.ip,
            "snmp_group": self.snmp_group,
            "alive": self.alive,
            "snmp": self.snmp,
            "ssh": self.ssh,
            "mysql": self.mysql,
            "mysql_user": self.mysql_user,
            "mysql_password": self.mysql_password,
            "uname": self.uname,
            "errors": self.errors,
            "scanned": self.scanned
        }

    @staticmethod
    def from_dict(dict_device: dict) -> 'Device':
        """Creates a Device object from a dictionary."""
        return Device(
            id=dict_device['id'],
            host=str(dict_device['host']),
            ip=str(dict_device['ip']),
            snmp_group=str(dict_device['snmp_group']),
            alive=dict_device['alive'],
            snmp=dict_device['snmp'],
            ssh=dict_device['ssh'],
            mysql=dict_device['mysql'],
            mysql_user=str(dict_device['mysql_user']),
            mysql_password=str(dict_device['mysql_password']),
            uname=str(dict_device['uname']),
            errors=dict_device['errors'],
            scanned=dict_device['scanned']
        )

    def status(self) -> str:
        """Returns a string summarizing the device's status."""
        return f"{self.host} -> alive: {self.alive}, ssh: {self.ssh}, snmp: {self.snmp}, mysql: {self.mysql}, info: {', '.join(self.errors)}"

    def __repr__(self) -> str:
        """Returns a string representation of the device."""
        return f"{self.host} ({self.ip})"

    def __str__(self) -> str:
        """Returns a JSON string representation of the device."""
        return str(self.to_dict())


class SSHHelper:
    """Helper class to manage SSH connections and commands."""

    @staticmethod
    @defer.inlineCallbacks
    def connect_and_run(host: str, user: str, command: str) -> defer.Deferred:
        """Connects to the host via SSH and runs a command."""
        ssh = SSHClient()
        ssh.load_host_keys(KEY_FILE)
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            ssh.connect(host, username=user, timeout=3)
            stdin, stdout, stderr = ssh.exec_command(command)
            result = stdout.read().decode().strip()
            defer.returnValue(result)
        except (AuthenticationException, SSHException) as e:
            logger.error(f"(ssh) {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"(ssh) {str(e)}")
            raise e
        finally:
            ssh.close()


class MySQLHelper:
    """Helper class to manage MySQL connections and queries."""

    @staticmethod
    @defer.inlineCallbacks
    def check_mysql(host: str, user: str, password: str) -> defer.Deferred:
        """Checks if MySQL is available on the device."""
        db = adbapi.ConnectionPool(
            'MySQLdb',
            host=host,
            user=user,
            passwd=password,
            db='mysql'
        )
        try:
            cursor = yield db.runQuery("SELECT VERSION()")
            if cursor:
                defer.returnValue(True)
            else:
                defer.returnValue(False)
        except MySQLdb.OperationalError as e:
            logger.error(f"(mysql) {str(e)}")
            raise e
        finally:
            yield db.close()


class SNMPAgent:
    """Helper class to manage SNMP interactions."""

    @staticmethod
    @defer.inlineCallbacks
    def check_snmp(host: str, snmp_group: str) -> defer.Deferred:
        """Checks if SNMP is available on the device."""
        load("SNMPv2-MIB")
        try:
            m = M(host=host, community=snmp_group, version=2, timeout=2)
            if m.sysName is not None:
                defer.returnValue(True)
            else:
                defer.returnValue(False)
        except Exception as e:
            logger.error(f"(snmp) {str(e)}")
            raise e
