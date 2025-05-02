import asyncio
from bleak import BleakScanner

def detection_callback(device, advertisement_data):
    if device.name.startswith("PicoBeacon"):
        print(f"[FOUND] {device.name or 'Unknown'} - RSSI: {device.rssi} - Address: {device.address}")
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
        print("\nScan stopped.")
        await scanner.stop()

if __name__ == "__main__":
    asyncio.run(scan())
