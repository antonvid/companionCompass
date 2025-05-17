import asyncio
from bleak import BleakScanner
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Constants for distance calculation
A = 17.48043210453444
m = -1.8071351056155527

async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        try:
            if device.name and device.name.startswith("PicoBeacon"):
                rssi = abs(advertising_data.rssi)
                dist = 10 ** ((A - rssi) / (10 * m)) / 100
                logging.info(f"Device: {device.name}, Distance: {dist:.2f}m, RSSI: {advertising_data.rssi}")
        except Exception as e:
            logging.error(f"Error in callback: {e}")

    async with BleakScanner(callback, filters={"DuplicateData": True}) as scanner:
        try:
            logging.info("Scanning for BLE beacons... Press Ctrl+C to stop.")
            await asyncio.wait_for(stop_event.wait(), timeout=60)  # Timeout after 60 seconds
        except asyncio.TimeoutError:
            logging.info("Scan timed out after 60 seconds.")
        except asyncio.CancelledError:
            logging.info("Scan cancelled.")
        finally:
            logging.info("Stopping scan...")
            await scanner.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")