import csv
import sqlite3
from typing import List
from jinja2 import Environment, FileSystemLoader
from device import Device
import spreadsheet


class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def __del__(self):
        self.connection.close()

    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS devices;")
        self.cursor.execute('''CREATE TABLE devices (
                                id INTEGER PRIMARY KEY,
                                host VARCHAR(255),
                                ip VARCHAR(255),
                                snmp_group VARCHAR(255),
                                alive BOOL,
                                snmp BOOL,
                                ssh BOOL,
                                errors VARCHAR(255),
                                mysql BOOL,
                                mysql_user VARCHAR(255),
                                mysql_password VARCHAR(255),
                                uname VARCHAR(255),
                                scanned BOOL
                          );''')

    def get_all_devices(self) -> List[Device]:
        devices = []
        for row in self.cursor.execute('SELECT * FROM devices'):
            device = Device(*row)
            devices.append(device)
        return devices

    def update_device(self, device: Device) -> None:
        sql = '''UPDATE devices
                 SET alive = ?, snmp = ?, ssh = ?, errors=?, mysql = ?, uname = ?, scanned = ?
                 WHERE id = ?'''
        data = [device.alive, device.snmp, device.ssh, device.ssh_error,
                device.mysql, device.uname, device.scanned, device.id]
        self.cursor.execute(sql, data)
        self.connection.commit()

    def insert_device(self, host: str, ip: str, snmp_group: str, mysql_user: str, mysql_password: str) -> None:
        sql = '''INSERT INTO devices (host, ip, snmp_group, alive, snmp, ssh,
                                      mysql, mysql_user, mysql_password, uname, scanned)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        data = [host, ip, snmp_group, False, False, False, False,
                mysql_user, mysql_password, "", False]
        self.cursor.execute(sql, data)


class Exporter:
    def __init__(self, devices: List[Device]):
        self.devices = devices

    def to_excel(self, filename: str) -> None:
        spreadsheet.export_to_xlsx(self.devices, filename)

    def to_csv(self, filename: str) -> None:
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for device in self.devices:
                writer.writerow([device.host, device.ip, device.snmp_group,
                                 device.alive, device.snmp, device.ssh,
                                 device.mysql, device.uname])

    def to_html(self, filename: str) -> None:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('layout.html')
        output_from_parsed_template = template.render(devices=self.devices)

        with open(filename, "w") as output:
            output.write(output_from_parsed_template)


class DeviceManager:
    def __init__(self, database_name):
        self.database = Database(database_name)

    def add_device(self, host: str, ip: str, snmp_group: str, mysql_user: str, mysql_password: str) -> None:
        self.database.insert_device(host, ip, snmp_group, mysql_user, mysql_password)

    def update_device(self, device: Device) -> None:
        self.database.update_device(device)

    def get_all_devices(self) -> List[Device]:
        return self.database.get_all_devices()

    def export_to_excel(self, filename: str) -> None:
        devices = self.get_all_devices()
        exporter = Exporter(devices)
        exporter.to_excel(filename)

    def export_to_csv(self, filename: str) -> None:
        devices = self.get_all_devices()
        exporter = Exporter(devices)
        exporter.to_csv(filename)

    def export_to_html(self, filename: str) -> None:
        devices = self.get_all_devices()
        exporter = Exporter(devices)
        exporter.to_html(filename)

class Importer:
    def __init__(self, database_name):
        self.database = Database(database_name)

    def from_csv(self, csv_file: str) -> None:
        with open(csv_file, 'r') as csv_input:
            csv_reader = csv.reader(csv_input, delimiter=',')
            for row in csv_reader:
                self.database.insert_device(*row[0:4], *row[8:10])
        self.database.connection.commit()


if __name__ == '__main__':
    manager = DeviceManager(database_name='devices.db')
    exporter = Exporter(devices=manager.get_all_devices())

    # Add a new device
    manager.add_device('new-host', '192.168.0.1', 'public', 'user', 'password')

    # Update an existing device
    devices = manager.get_all_devices()
    if devices:
        device = devices[0]
        device.alive = True
        device.snmp = True
        device.ssh = True
        manager.update_device(device)

    # Export to Excel
    exporter.to_excel(filename='devices.xlsx')

    # Export to CSV
    exporter.to_csv(filename='devices.csv')

    # Export to HTML
    exporter.to_html(filename='devices.html')

    # Import from CSV
    importer = Importer(database_name='devices.db')
    importer.from_csv(csv_file='new-devices.csv')
