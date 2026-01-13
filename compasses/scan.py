import asyncio
from bleak import BleakScanner

async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        try:
            if device.name and device.name.startswith("beacon"):
                print(f"Device: {device.name}, RSSI: {advertising_data.rssi}")
        except Exception as e:
            print(f"Error in callback: {e}")

    async with BleakScanner(callback, scanning_mode="active") as scanner:
        try:
            print("Scanning for BLE beacons... Press Ctrl+C to stop.")
            await stop_event.wait()
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