import asyncio
import csv
from bleak import BleakScanner

dist = input("Enter distance from b1: ")

# open CSV for writing RSSI data
csv_file = open(f"rssi_data_{dist}b1.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Beacon", "RSSI"]) # header row

def detection_callback(device, advertisement_data):
    if device.name and device.name.startswith("PicoBeacon"):
        print(f"[FOUND] {device.name or 'Unknown'} - RSSI: {advertisement_data.rssi} - Address: {device.address}")
        # write data to CSV
        csv_writer.writerow([device.name, advertisement_data.rssi])
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
    finally:
        csv_file.close()

if __name__ == "__main__":

    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        print("Stopped by user")