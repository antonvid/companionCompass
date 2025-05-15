import asyncio
from bleak import BleakScanner
import time

# constants for distance calculation
A = 15.284055464858218
m = -1.9382076537407522


def detection_callback(device, advertisement_data):

    if device.name and device.name.startswith("PicoBeacon"):

        rssi = abs(advertisement_data.rssi)
        dist = 10 ** ((A - rssi) / (10 * m))
        dist = dist/100

        print(f"{dist:.2f}m")

async def scan():
    scanner = BleakScanner(detection_callback)
    print("Scanning for BLE beacons... Press Ctrl+C to stop.")
    await scanner.start()
    try:
        while True:
            await asyncio.sleep(0.1) 
    except KeyboardInterrupt:
        await scanner.stop()

if __name__ == "__main__":
    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        print("Stopped by user")