import logging
from twisted.internet import defer, reactor
from devices import Device

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
twisted_log.PythonLoggingObserver().start()

@defer.inlineCallbacks
def main():
    device = Device(id=1, host="192.168.1.1", ip="192.168.1.1")
    yield device.scan()
    print(device.status())
    reactor.stop()

if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
