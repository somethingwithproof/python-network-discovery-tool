#!/usr/bin/env python
import argparse
import database
import logging
import threading
import math
from devices import test_ssh, test_ping, ScanTypes
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    filename='discover.log',
                    level=logging.DEBUG)

DATABASE = 'devices.db'
MAX_WORKERS = 10

def check_params():
    parser = argparse.ArgumentParser(description='Discover info of network' +
                                                 'devices.')
    parser.add_argument('inputfile', help='excel file with hosts to scan')

    return parser.parse_args()


def how_many_workers(items):
    if len(items) < MAX_WORKERS:
        workers = len(items)
    else:
        workers = MAX_WORKERS

    return workers


def get_intervals(items, workers):
    max_devices = int(math.ceil(len(items) / float(workers)))

    return [items[x:x+max_devices] for x in range(0, len(items), max_devices)]


def scan(devices):
    logging.info("Starting worker to process {} devices".format(len(devices)))
    device_dict = {device.id:device for device in devices}
    
    futures = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Dispatch all of the tests
        for device in devices:
            logging.info("Scanning device: {}".format(device))
            # device.scan()
            futures.append(executor.submit(test_ping, device))
            futures.append(executor.submit(test_ssh, device))
            # logging.info("Scanning result for device: {}".format(device))
            # lock.acquire()
            # database.update_device(DATABASE, device)
            # lock.release()
        
        # As results come in, update the device objects
        for future in as_completed(futures):
            result = future.result()
            update_device(result, device_dict[result.device_id])
            
def update_device(result, device):
    if (result.type == ScanTypes.ping):
        device.alive = not result.errors
    if (result.type == ScanTypes.ssh):
        device.ssh = not result.errors
    device.errors = result.errors

if __name__ == "__main__":
    args = check_params()

    logging.info("Create database")
    database.create(DATABASE)
    logging.info("Import excel to database")
    database.import_excel(DATABASE, args.inputfile)
    logging.info("Read devices for database")
    devices = database.get_all_devices(DATABASE)

    workers = how_many_workers(devices)
    intervals = get_intervals(devices, workers)

    # start workers
    threads = list()
    for interval in intervals:
        t = threading.Thread(target=scan, args=(interval,))
        threads.append(t)
        t.start()

    # wait for all workers
    logging.info("Waiting for all workers")
    for t in threads:
        t.join()

    logging.info("All workers are done")

    # Exporting data
    devices = database.get_all_devices(DATABASE)
    logging.info("Exporting to excel")
    database.export_excel(devices)

    logging.info("Updating input")
    database.update_excel(args.inputfile, devices)
