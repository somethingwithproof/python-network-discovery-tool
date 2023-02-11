import csv
import sqlite3
from jinja2 import Environment, FileSystemLoader
from device import Device
import spreadsheet


def create_database(database_name: str) -> None:
    """
    Creates a SQLite database. If a database with the same name already exists,
    it will be dropped and a new database will be created.
    
    :param database_name: The name of the database to be created.
    :return: None
    """
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS devices;")
    cursor.execute('''CREATE TABLE devices (
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
    conn.commit()
    conn.close()


def get_all_devices(database_name: str) -> List[Device]:
    """
    Retrieves all devices from the database.
    
    :param database_name: The name of the database.
    :return: A list of `Device` objects.
    """
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    devices = []
    for row in cursor.execute('SELECT * FROM devices'):
        device = Device(*row)
        devices.append(device)
    conn.close()
    return devices


def update_device(database_name: str, device: Device) -> None:
    """
    Updates a device in the database.
    
    :param database_name: The name of the database.
    :param device: The `Device` object to be updated.
    :return: None
    """
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    sql = '''UPDATE devices
             SET alive = ?, snmp = ?, ssh = ?, errors=?, mysql = ?, uname = ?, scanned = ?
             WHERE id = ?'''
    data = [device.alive, device.snmp, device.ssh, device.ssh_error,
            device.mysql, device.uname, device.scanned, device.id]
    cursor.execute(sql, data)
    conn.commit()
    conn.close()


def insert_device(cursor, host: str, ip: str, snmp_group: str, mysql_user: str, mysql_password: str) -> None:
    """
    Insert a new device into the database.

    Args:
        cursor: SQLite3 cursor object
        host: Hostname of the device
        ip: IP address of the device
        snmp_group: SNMP group of the device
        mysql_user: MySQL username for the device
        mysql_password: MySQL password for the device

    Returns:
        None
    """
    sql = '''INSERT INTO devices (host, ip, snmp_group, alive, snmp, ssh,
                                  mysql, mysql_user, mysql_password, uname, scanned)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = [host, ip, snmp_group, False, False, False, False,
            mysql_user, mysql_password, "", False]
    cursor.execute(sql, data)


def export_excel(devices: List[Device]) -> None:
    spreadsheet.export_to_xlsx(devices)


def update_excel(excel_file: str, devices: List[Device]) -> None:
    spreadsheet.add_chek(excel_file, devices)


def import_csv(database_name: str, csv_file: str) -> None:
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    with open(csv_file, 'r') as csv_input:
        csv_reader = csv.reader(csv_input, delimiter=',')
        for row in csv_reader:
            insert_device(cursor, row[0], row[2], row[3], row[8], row[9])

    conn.commit()
    conn.close()


def export_csv(database_name: str, csv_file: str) -> None:
    devices = get_all_devices(database_name)

    with open(csv_file, 'wb') as csv_output:
        writer = csv.writer(csv_output, delimiter=',')
        for device in devices:
            writer.writerow([device.host, device.ip, device.snmp_group,
                             device.alive, device.snmp, device.ssh,
                             device.mysql, device.uname])


def export_html(database_name: str, html_file: str) -> None:
    devices = get_all_devices(database_name)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('layout.html')
    output_from_parsed_template = template.render(devices=devices)

    with open(html_file, "wb") as output:
        output.write(output_from_parsed_template)
