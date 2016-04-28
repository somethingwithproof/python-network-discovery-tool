import sqlite3
import csv
from jinja2 import Environment, FileSystemLoader
from device import Device
import spreadsheet


def create(database_name):
    conn = sqlite3.connect(database_name)

    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS devices;")
    c.execute('''CREATE TABLE devices (
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


def get_all_devices(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    devices = []
    for row in c.execute('SELECT * FROM devices'):
        device = Device(row[0], row[1], row[2], row[3], row[4], row[5],
                        row[6], row[7], row[8], row[9], row[10], row[11],
                        row[12])
        devices.append(device)
    conn.close()
    return devices


def update_device(database_name, device):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    sql = '''UPDATE devices
             SET alive = ?, snmp = ?, ssh = ?, errors=?, mysql = ?, uname = ?, scanned = ?
             WHERE id = ?'''
    data = [device.alive, device.snmp, device.ssh, device.ssh_error,
            device.mysql, device.uname, device.scanned, device.id]
    c.execute(sql, data)
    conn.commit()
    conn.close()


def insert_device(cursor, host, ip, snmp_group, mysql_user, mysql_password):
    sql = '''INSERT INTO devices (host, ip, snmp_group, alive, snmp, ssh,
                                  mysql, mysql_user, mysql_password, uname, scanned)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = [host, ip, snmp_group, False, False, False, False,
            mysql_user, mysql_password, "", False]
    cursor.execute(sql, data)


def import_excel(database_name, excel_file):
    devices = spreadsheet.get_all_devices(excel_file)

    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    for device in devices:
        insert_device(c, device.host, device.ip, device.snmp_group,
                      device.mysql_user, device.mysql_password)

    conn.commit()
    conn.close()


def export_excel(devices):
    spreadsheet.export_to_xlsx(devices)


def update_excel(excel_file, devices):
    spreadsheet.add_chek(excel_file, devices)


def import_csv(database_name, csv_file):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    with open(csv_file, 'r') as csv_input:
        csv_reader = csv.reader(csv_input, delimiter=',')
        for row in csv_reader:
            insert_device(c, row[0], row[2], row[3], row[8], row[9])

    conn.commit()
    conn.close()


def export_csv(database_name, csv_file):
    devices = get_all_devices(database_name)

    with open(csv_file, 'wb') as csv_output:
        writer = csv.writer(csv_output, delimiter=',')
        for device in devices:
            writer.writerow([device.host, device.ip, device.snmp_group,
                             device.alive, device.snmp, device.ssh,
                             device.mysql, device.uname])


def export_html(database_name, html_file):
    devices = get_all_devices(database_name)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('layout.html')
    output_from_parsed_template = template.render(devices=devices)

    with open(html_file, "wb") as output:
        output.write(output_from_parsed_template)
