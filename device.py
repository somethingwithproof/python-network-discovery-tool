import subprocess
from snimpy.manager import Manager as M
from snimpy.manager import load
import paramiko
import MySQLdb
import socket
import json
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException


USER = 'zenossmon'
KEY_FILE = '/home/efren/.ssh/id_rsa.pub'


class Device:

    def __init__(self, id, host, ip, snmp_group="", alive=False,
                 snmp=False, ssh=False, mysql=False, mysql_user="",
                 mysql_password="", uname="", errors="", scanned=False):
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
        self.ssh_open = False
        self.errors = errors
        self.mysql = mysql == 1
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_open = False
        self.uname = uname
        self.scanned = scanned

    def record(self, redis=None):
        redis.set(self.key(), self.to_json())

    def scan(self, redis=None):
        self.is_alive()
        self.record(redis)

        if self.alive:
            self.has_snmp()
            self.record(redis)
            self.has_ssh()
            self.record(redis)
            if self.mysql_user != "" and self.mysql_user is not None:
                self.has_mysql()
            else:
                self.has_error("(mysql) Don't have connection data")
        else:
            self.ssh = False
            self.snmp = False
            self.mysql = False
            self.uname = "unknown"
            self.has_error("(alive) Host is down")

        self.record(redis)
        self.scanned = True

    def has_error(self, msg):
        if self.errors == "" or self.errors is None:
            self.errors = msg
        else:
            self.errors = self.errors + ", " + msg

    def is_alive(self):
        self.alive = False
        nmproc = NmapProcess(str(self.ip), '-sn')
        rc = nmproc.run()
        if rc != 0:
            self.has_error("(alive) {}".format(nmproc.stderr))
        else:
            nmap_report = NmapParser.parse(nmproc.stdout)
            self.alive = (nmap_report.hosts[0].status == 'up')

    def is_port_open(self, port):
        nmproc = NmapProcess(str(self.ip), '-p ' + str(port))

        rc = nmproc.run()
        if rc != 0:
            self.has_error("nmap scan failed: {0}".format(nmproc.stderr))
            return False
        else:
            nmap_report = NmapParser.parse(nmproc.stdout)
            if nmap_report.hosts[0].status == 'up':
                return (nmap_report.hosts[0].services[0].state == 'open')
            else:
                return False

    def has_ssh(self):
        self.ssh = False
        self.uname = "unknown"
        if not self.is_port_open(22):
            self.has_error("(ssh) Port closed")
            return

        ssh = paramiko.SSHClient()
        ssh.load_host_keys(KEY_FILE)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(str(self.host), username=USER, timeout=3)
            stdin, stdout, stderr = ssh.exec_command('uname -a')
            self.uname = stdout.read()
            self.ssh = True
        except Exception, e:
            self.has_error("(ssh) " + e.message)

    def has_snmp(self):
        load("SNMPv2-MIB")
        self.snmp = False
        try:
            m = M(host=str(self.host), community=str(self.snmp_group),
                  version=2, timeout=2)
            if m.sysName is not None:
                self.snmp = True
        except Exception, e:
            self.has_error("(snmp) " + e.message)
            self.snmp = False

    def has_mysql(self):
        self.mysql = False
        if not self.port_open(3306):
            self.has_error("(mysql) Port closed")
            return
        try:
            db = MySQLdb.connect(str(self.host), str(self.mysql_user), str(self.mysql_password))
            cursor = db.cursor()
            cursor.execute("SELECT VERSION()")
            results = cursor.fetchone()
            # Check if anything at all is returned
            if results:
                self.mysql = True
            db.close()
        except MySQLdb.Error, e:
            self.has_error("(mysql) " + e.__str__())

    def key(self):
        return "device:{}".format(self.id)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        device_dict = {
            "id":             self.id,
            "host":           self.host,
            "ip":             self.ip,
            "snmp_group":     self.snmp_group,
            "alive":          self.alive,
            "snmp":           self.snmp,
            "ssh":            self.ssh,
            "mysql":          self.mysql,
            "mysql_user":     self.mysql_user,
            "mysql_password": self.mysql_password,
            "uname":          self.uname,
            "errors":         self.errors,
            "scanned":        self.scanned
        }
        return device_dict

    @staticmethod
    def from_dict(dict_device):
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
            errors=str(dict_device['errors']),
            scanned=dict_device['scanned']
        )

    def status(self):
        return "{} -> alive: {}, ssh: {}, snmp: {}, mysql: {}, info: {}".format(self.host, self.alive, self.ssh,
                                                                                self.snmp, self.mysql, self.errors)

    def __repr__(self):
        return "{0} ({1})".format(self.host, self.ip)

    def __str__(self):
        return str(self.to_dict())
