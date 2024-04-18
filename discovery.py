#!/usr/bin/env python
import argparse
import os
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio
import device_module as devices
import database

# Constants
DATABASE = 'devices.db'
MAX_WORKERS = 10

def setup_logging():
    """
    Set up logging configuration for the application.
    
    This function configures the logging settings to write logs with a specific format
    and date format to a file named 'discover.log' at DEBUG level.
    """
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p',
        filename='discover.log',
        level=logging.DEBUG
    )

def parse_arguments():
    """
    Parse command line arguments to get the input Excel file.

    Returns:
        argparse.Namespace: The parsed arguments with 'inputfile' attribute which contains
                            the path to the input Excel file.
    """
    parser = argparse.ArgumentParser(description='Discover info of network devices.')
    parser.add_argument('inputfile', help='Excel file with hosts to scan')
    return parser.parse_args()

async def scan_device(device):
    """
    Asynchronously scan a single device using ping and SSH checks.

    Args:
        device (Device): A device object to perform network tests on.

    Returns:
        tuple: A tuple containing results of ping and SSH tests.
    """
    ping_result = await devices.test_ping(device)
    ssh_result = await devices.test_ssh(device)
    return (ping_result, ssh_result)

async def update_device_status(results):
    """
    Update device status based on the results of asynchronous network scans.

    Args:
        results (list of tuples): A list of tuples, each containing results of network tests
                                  performed on devices.

    This function updates each device's status attributes based on the results
    of the ping and SSH tests.
    """
    for result, device in results:
        if result.type == devices.ScanTypes.ping:
            device.alive = not result.errors
        elif result.type == devices.ScanTypes.ssh:
            device.ssh = not result.errors
        device.errors = result.errors

async def handle_devices(devices):
    """
    Handle the scanning and updating of multiple devices asynchronously.

    Args:
        devices (list of Device): A list of devices to scan.

    This function manages the asynchronous scanning and updating of a list of devices,
    collecting and passing results to be processed.
    """
    tasks = [asyncio.create_task(scan_device(device)) for device in devices]
    results = await asyncio.gather(*tasks)
    await update_device_status(results)

def main():
    """
    Main function to orchestrate the scanning of network devices.
    
    This function setups up logging, parses command line arguments, initiates
    and manages the database connections, and controls the flow of device scanning
    and result processing.
    """
    setup_logging()
    args = parse_arguments()

    logging.info("Creating database")
    with database.create(DATABASE) as db:
        logging.info("Importing excel to database")
        database.import_excel(db, args.inputfile)

    logging.info("Reading devices from database")
    with database.get_connection(DATABASE) as db:
        device_list = database.get_all_devices(db)

    asyncio.run(handle_devices(device_list))

    logging.info("All workers have completed")
    with database.get_connection(DATABASE) as db:
        updated_devices = database.get_all_devices(db)
        logging.info("Exporting to excel")
        database.export_excel(updated_devices)

    logging.info("Updating input")
    output_file = os.path.join(os.path.dirname(args.inputfile), 'output.xlsx')
    database.update_excel(output_file, updated_devices)

if __name__ == "__main__":
    main()
