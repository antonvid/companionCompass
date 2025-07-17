import asyncio
from bleak import BleakScanner

# Constants for distance calculation
A = 17.48043210453444
m = -1.8071351056155527

async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        try:
            if device.name and device.name.startswith("beacon"):
                rssi = abs(advertising_data.rssi)
                dist = 10 ** ((A - rssi) / (10 * m)) / 100
                print(f"Device: {device.name}, Distance: {dist:.2f}m, RSSI: {advertising_data.rssi}")
        except Exception as e:
            print(f"Error in callback: {e}")

    async with BleakScanner(callback, filters={"DuplicateData": True}) as scanner:
        try:
            print("Scanning for BLE beacons... Press Ctrl+C to stop.")
            await asyncio.wait_for(stop_event.wait(), timeout=60)  # Timeout after 60 seconds
        except asyncio.TimeoutError:
            print("Scan timed out after 60 seconds.")
        except asyncio.CancelledError:
            print("Scan cancelled.")
        finally:
            print("Stopping scan...")
            await scanner.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")