import asyncio
from bleak import BleakScanner

def detection_callback(device, advertisement_data):
    if device.name and device.name.startswith("PicoBeacon"):
        rssi = abs(advertisement_data.rssi)
        A = 15.284055464858218
        m = -1.9382076537407522

        dist = 10 ** ((A - rssi) / (10 * m))

        print(f"[FOUND] {device.name or 'Unknown'} - RSSI: {rssi} - Address: {device.address} - Distance: {dist}cm")
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