#!/usr/bin/env python
import argparse
import store
import spreadsheet
import logging
import math
import threading

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    #filename='discover.log',
                    level=logging.DEBUG)

MAX_WORKERS = 10
lock = threading.Lock()


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
    redis = store.get_redis()
    logging.info("Starting worker to process {} devices".format(len(devices)))
    for device in devices:
        logging.info("Scanning device: {}".format(device))
        device.scan(lock, redis=redis)
        for e in device.errors:
            print("ERROR ", device, e)
        logging.info("Scanning result for device: {}".format(device))

if __name__ == "__main__":
    args = check_params()

    logging.info("Import excel")
    devices = spreadsheet.import_from_excel(args.inputfile)
    logging.info("Store devices in Redis")
    store.save_devices(devices, flush=True)

    workers = how_many_workers(devices)
    intervals = get_intervals(devices, workers)

    # start workers
    logging.info("Starting workers")
    threads = list()
    for interval in intervals[:100]:
        #t = threading.Thread(target=scan, args=(interval,))
        #threads.append(t)
        #t.start()
        scan(interval)

    # wait for all workers
    logging.info("Waiting for all workers")
    for t in threads:
        t.join()

    logging.info("All workers are done")

    # Exporting data
    devices = store.get_all_devices()

    logging.info("Export to html")
    store.export_html("html/output.html")

    logging.info("Export to csv")
    store.export_csv("devices.csv")

    logging.info("Updating excel input")
    spreadsheet.export_to_excel(devices, spreadsheet=args.inputfile)

    logging.info("Exporting to excel")
    spreadsheet.export_to_excel(devices)

