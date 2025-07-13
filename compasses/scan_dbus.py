import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import MessageType, BusType
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def parse_device(interface_props):
    """Extract device properties like name, address, and RSSI."""
    name = interface_props.get("Name", None)
    address = interface_props.get("Address", None)
    rssi = interface_props.get("RSSI", None)
    return name, address, rssi

async def scan_ble_beacons():
    # Connect to the system bus
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

    # Define a signal handler for BLE device discovery
    def signal_handler(message):
        if message.message_type != MessageType.SIGNAL or message.member != "InterfacesAdded":
            return

        path, interfaces = message.body
        device = interfaces.get("org.bluez.Device1")
        if not device:
            return

        # Parse device properties
        name, address, rssi = parse_device(device)
        if name and name.startswith("beacon"):
            logging.info(f"[FOUND] {name} | Address: {address} | RSSI: {rssi}")

    # Add the signal handler to the bus
    bus.add_message_handler(signal_handler)

    # Get the BLE adapter and start discovery
    try:
        introspection = await bus.introspect("org.bluez", "/org/bluez/hci0")
        obj = bus.get_proxy_object("org.bluez", "/org/bluez/hci0", introspection)
        adapter = obj.get_interface("org.bluez.Adapter1")

        await adapter.call_start_discovery()
        logging.info("Scanning for BLE beacons with names starting with 'beacon'...")

        # Keep the script running to listen for signals
        await asyncio.Future()
    except KeyboardInterrupt:
        logging.info("Stopping scan...")
        await adapter.call_stop_discovery()
    except Exception as e:
        logging.error(f"Error during BLE scanning: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(scan_ble_beacons())
    except Exception as e:
        logging.error(f"Unexpected error: {e}")