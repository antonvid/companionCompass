import asyncio
from bleak import BleakScanner
import time

# constants for distance calculation
A = 15.284055464858218
m = -1.9382076537407522

async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        if device.name and device.name.startswith("PicoBeacon"):
            rssi = abs(advertising_data.rssi)
            dist = 10 ** ((A - rssi) / (10 * m))
            dist = dist/100
            
            print(f"{device.name}: {dist:.2f}m") # print beacon name plus distance estimate

    async with BleakScanner(callback) as scanner:
        print("Scanning for BLE beacons... Press Ctrl+C to stop.")
        try:
            await stop_event.wait()
        except KeyboardInterrupt: # stop when Ctrl+C is pressed
            print("\nStopping scan")

if __name__ == "__main__":
    asyncio.run(main())