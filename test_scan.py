import redis
import json
from device import Device
import store

r = redis.Redis(host=store.REDIS_SERVER, db=store.REDIS_DB)
r.flushdb()

device = Device(id=1, host='localhost', ip='127.0.0.1', mysql_user='roo', mysql_password='admin')

device.scan(redis=r)

stored_devices = store.get_all_devices()

for device in stored_devices:
    print device.status()