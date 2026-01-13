"""
Scan/Discovery Async Iterator
--------------

Example showing how to scan for BLE devices using async iterator instead of callback function

Created on 2023-07-07 by bojanpotocnik <info@bojanpotocnik.com>

"""

import asyncio

from bleak import BleakScanner


async def main():
    async with BleakScanner() as scanner:
        print("Scanning...")

        async for bd, ad in scanner.advertisement_data():
            print(f" Found {bd!r} with {ad!r}")


if __name__ == "__main__":
    asyncio.run(main())
