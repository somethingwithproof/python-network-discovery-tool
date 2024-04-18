#!/usr/bin/env python
import argparse
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import device_module as devices  # Renamed to avoid naming conflict
import database

# Constants
DATABASE = 'devices.db'
MAX_WORKERS = 10

# Setup logging
def setup_logging():
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        filename='discover.log',
                        level=logging.DEBUG)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Discover info of network devices.')
    parser.add_argument('inputfile', help='excel file with hosts to scan')
    return parser.parse_args()

def determine_worker_count(items):
    return min(len(items), MAX_WORKERS)

def calculate_intervals(items, workers):
    max_devices_per_worker = (len(items) + workers - 1) // workers  # Use integer division ceiling
    return [items[i:i + max_devices_per_worker] for i in range(0, len(items), max_devices_per_worker)]

def scan(device_list):
    logging.info(f"Starting worker to process {len(device_list)} devices")
    device_dict = {device.id: device for device in device_list}
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_ping = {executor.submit(device.test_ping): device for device in device_list}
        future_ssh = {executor.submit(device.test_ssh): device for device in device_list}
        future_to_device = {**future_ping, **future_ssh}

        for future in as_completed(future_to_device):
            device = future_to_device[future]
            try:
                result = future.result()
                results.append(result)
                update_device_status(result, device)
            except Exception as e:
                logging.error(f"Failed to execute task for device {device.id}: {str(e)}")

def update_device_status(result, device):
    if result.type == devices.ScanTypes.ping:
        device.alive = not result.errors
    elif result.type == devices.ScanTypes.ssh:
        device.ssh = not result.errors
    device.errors = result.errors

def main():
    setup_logging()
    args = parse_arguments()

    logging.info("Creating database")
    with database.create(DATABASE) as db:
        logging.info("Importing excel to database")
        database.import_excel(db, args.inputfile)

    logging.info("Reading devices from database")
    with database.get_connection(DATABASE) as db:
        device_list = database.get_all_devices(db)

    workers = determine_worker_count(device_list)
    intervals = calculate_intervals(device_list, workers)

    # Start scanning in parallel
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(scan, intervals)

    logging.info("All workers have completed")

    # Exporting data
    with database.get_connection(DATABASE) as db:
        updated_devices = database.get_all_devices(db)
        logging.info("Exporting to excel")
        database.export_excel(updated_devices)

    logging.info("Updating input")
    output_file = os.path.join(os.path.dirname(args.inputfile), 'output.xlsx')
    database.update_excel(output_file, updated_devices)

if __name__ == "__main__":
    main()
