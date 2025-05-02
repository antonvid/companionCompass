import asyncio
from bleak import BleakScanner

def detection_callback(device, advertisement_data):
    if device.name and device.name.startswith("PicoBeacon"):
        print(f"[FOUND] {device.name or 'Unknown'} - RSSI: {advertisement_data.rssi} - Address: {device.address}")
    else:
        pass

async def scan():
    scanner = BleakScanner(detection_callback)
    print("Scanning for BLE beacons... Press Ctrl+C to stop.")
    await scanner.start()
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await scanner.stop()

if __name__ == "__main__":
    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        print("Stopped by user")