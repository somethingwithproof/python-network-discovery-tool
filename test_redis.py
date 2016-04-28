import redis
import json


def prueba(*args, **kwargs):
    print 'args: ', args, ' kwargs: ', kwargs

dict_device = {'id': 1, 'host': 'hostname', 'ssh': True, 'mysql': None}

r = redis.Redis(host='localhost')

print json.dumps(dict_device)
r.set("device", json.dumps(dict_device))

dict_device = {'id': 2, 'host': 'hostname2', 'ssh': True, 'mysql': None}
prueba(dict_device)
r.set("device", json.dumps(dict_device))

stored_device = json.loads(r.get("device"))

print stored_device
