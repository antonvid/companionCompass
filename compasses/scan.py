import asyncio
import csv
from bleak import BleakScanner

# Initialize csv_file and csv_writer as None
csv_file = None
csv_writer = None

distFile = input("Enter distance from b1: ")

# open CSV for writing RSSI data
if distFile:
    csv_file = open(f"rssi_data_{distFile}.csv", mode="w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Beacon", "RSSI"]) # header row

def detection_callback(device, advertisement_data):
    if device.name and device.name.startswith("PicoBeacon"):
        rssi = advertisement_data.rssi
        A = 15.284055464858218
        m = -1.9382076537407522

        dist = 10 ** ((A - rssi) / (10 * m))

        print(f"[FOUND] {device.name or 'Unknown'} - RSSI: {rssi} - Address: {device.address} - Distance: {dist}cm")
        # write data to CSV
        if csv_writer:
            csv_writer.writerow([device.name, rssi])
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
        if csv_file:
            csv_file.close()

if __name__ == "__main__":

    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        print("Stopped by user")