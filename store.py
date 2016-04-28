import redis
import json
import csv
from jinja2 import Environment, FileSystemLoader
from device import Device

REDIS_SERVER = 'localhost'
REDIS_DB = 5


def get_redis():
    return redis.Redis(host=REDIS_SERVER, db=REDIS_DB)


def get_all_devices():
    r = get_redis()
    devices = []
    for key in r.scan_iter(match='device:*'):
        dict_device = json.loads(r.get(key))
        device = Device.from_dict(dict_device)
        devices.append(device)
    return devices


def save_devices(devices, flush=False):
    r = get_redis()
    if flush:
        r.flushdb()

    for device in devices:
        r.set(device.key(), device.to_json())


def export_csv(csv_file):
    devices = get_all_devices()

    with open(csv_file, 'wb') as csv_output:
        writer = csv.writer(csv_output, delimiter=',')
        for device in devices:
            writer.writerow([device.host, device.ip, device.snmp_group,
                             device.alive, device.snmp, device.ssh,
                             device.mysql, device.uname, device.errors])


def export_html(html_file):
    devices = get_all_devices()
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('layout.html')
    output_from_parsed_template = template.render(devices=devices)

    with open(html_file, "wb") as output:
        output.write(output_from_parsed_template)
