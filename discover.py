import json
from twisted.internet import reactor, defer
from devices import DeviceManager
from device import Device

@defer.inlineCallbacks
def discover_devices():
    """Discovers devices and returns their status."""
    manager = DeviceManager()

    device1 = Device(id=1, host="192.168.1.1", ip="192.168.1.1")
    device2 = Device(id=2, host="192.168.1.2", ip="192.168.1.2")

    manager.add_device(device1)
    manager.add_device(device2)

    yield device1.scan()
    yield device2.scan()

    result = manager.to_dict()
    defer.returnValue(result)

@defer.inlineCallbacks
def main():
    devices = yield discover_devices()
    print(json.dumps(devices, indent=2))
    reactor.stop()

if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
