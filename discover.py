#!/usr/bin/env python
import argparse
import logging
from math import ceil
from pathlib import Path
import asyncio
import aioredis
import aiohttp

import store
import spreadsheet

# Constants
DATABASE = 'devices.db'
MAX_WORKERS = 10

def setup_logging():
    """
    Configure the logging settings for the application.
    This function sets up logging to output with a specified format and date format.
    """
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p',
        level=logging.DEBUG
    )

class AsyncDataStore:
    """
    Class to handle asynchronous data storage interactions with Redis.
    """
    @staticmethod
    async def get_redis():
        """
        Establish an asynchronous connection to Redis.
        
        Returns:
            aioredis.Connection: An asynchronous Redis connection pool.

        Raises:
            Exception: If the connection to Redis fails.
        """
        try:
            return await aioredis.create_redis_pool('redis://localhost')
        except Exception as e:
            logging.error(f"Failed to connect to Redis asynchronously: {e}")
            raise

    @staticmethod
    async def save_devices(devices):
        """
        Save a list of devices to Redis asynchronously.

        Args:
            devices (list): A list of device objects to be saved in Redis.
        """
        redis = await AsyncDataStore.get_redis()
        await redis.multi_exec(*(store.save_device_async(device) for device in devices))
        redis.close()
        await redis.wait_closed()

    @staticmethod
    async def get_all_devices():
        """
        Retrieve all devices from Redis asynchronously.

        Returns:
            list: A list of device objects retrieved from Redis.
        """
        redis = await AsyncDataStore.get_redis()
        devices = await store.get_all_devices_async(redis)
        redis.close()
        await redis.wait_closed()
        return devices

class SpreadsheetHandler:
    """
    Class to manage spreadsheet operations for importing and exporting device data.
    """
    @staticmethod
    def import_from_excel(file_path: Path):
        """
        Import devices from an Excel file.

        Args:
            file_path (Path): The path to the Excel file.

        Returns:
            list: A list of imported device objects.

        Raises:
            Exception: If there is an error in importing from Excel.
        """
        try:
            return spreadsheet.import_from_excel(str(file_path))
        except Exception as e:
            logging.error(f"Error importing from Excel: {e}")
            raise

    @staticmethod
    def export_to_excel(devices: list, file_path: Path):
        """
        Export devices to an Excel file.

        Args:
            devices (list): A list of device objects to be exported.
            file_path (Path): The path to the Excel file where data will be saved.

        Raises:
            Exception: If there is an error in exporting to Excel.
        """
        try:
            spreadsheet.export_to_excel(devices, spreadsheet=str(file_path))
        except Exception as e:
            logging.error(f"Error exporting to Excel: {e}")
            raise

class AsyncDeviceScanner:
    """
    Class to handle asynchronous device scanning logic using aiohttp.
    """
    def __init__(self, devices):
        """
        Initialize the AsyncDeviceScanner with a list of devices.

        Args:
            devices (list): A list of devices to scan.
        """
        self.devices = devices

    async def scan_devices(self):
        """
        Scan a group of devices asynchronously and log their processing.
        """
        redis = await AsyncDataStore.get_redis()
        logging.info(f"Starting worker to process {len(self.devices)} devices")
        async with aiohttp.ClientSession() as session:
            tasks = [self.scan_device(device, session, redis) for device in self.devices]
            await asyncio.gather(*tasks)

    async def scan_device(self, device, session, redis):
        """
        Perform an asynchronous scan on a single device using an HTTP session and Redis connection.

        Args:
            device (Device): The device object to scan.
            session (aiohttp.ClientSession): The HTTP session to use for network calls.
            redis (aioredis.Connection): The Redis connection to use for storing data.

        Raises:
            Exception: If an error occurs during the device scan.
        """
        try:
            await device.async_scan(session, redis)
            logging.info(f"Scanning completed for device: {device}")
        except Exception as e:
            logging.error(f"Exception scanning device {device}: {e}")

def parse_arguments():
    """
    Parse command line arguments for the script.

    Returns:
        argparse.Namespace: The parsed arguments, including the path to the input Excel file.
    """
    parser = argparse.ArgumentParser(description='Discover information about network devices.')
    parser.add_argument('inputfile', type=Path, help='Excel file with hosts to scan')
    return parser.parse_args()

def distribute_work(items, workers):
    """
    Divide items into even chunks for each worker.

    Args:
        items (list): A list of items to distribute.
        workers (int): The number of workers.

    Returns:
        list of list: A list containing sublists of items, each sublist corresponds to a worker's load.
    """
    chunk_size = ceil(len(items) / workers)
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

async def main():
    """
    Main function to orchestrate the asynchronous scanning of network devices.
    Manages the import, processing, and export of device data.
    """
    setup_logging()
    args = parse_arguments()

    devices = SpreadsheetHandler.import_from_excel(args.inputfile)
    await AsyncDataStore.save_devices(devices)

    worker_count = min(len(devices), MAX_WORKERS)
    work_chunks = distribute_work(devices, worker_count)

    await asyncio.gather(*(AsyncDeviceScanner(chunk).scan_devices() for chunk in work_chunks))

    logging.info("All workers have completed")
    updated_devices = await AsyncDataStore.get_all_devices()
    SpreadsheetHandler.export_to_excel(updated_devices, args.inputfile)

if __name__ == "__main__":
    asyncio.run(main())
