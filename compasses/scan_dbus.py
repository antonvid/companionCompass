import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import MessageType, BusType

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
        if message.message_type != MessageType.SIGNAL:
            return
        if message.member != "InterfacesAdded":
            return
        path, interfaces = message.body
        device = interfaces.get("org.bluez.Device1")
        if not device:
            return

        # Parse device properties
        name, address, rssi = parse_device(device)
        if name and name.startswith("PicoBeacon"):
            print(f"[FOUND] {name} | Address: {address} | RSSI: {rssi}")

    # Add the signal handler to the bus
    bus.add_message_handler(signal_handler)

    # Get the BLE adapter and start discovery
    introspection = await bus.introspect("org.bluez", "/org/bluez/hci0")
    obj = bus.get_proxy_object("org.bluez", "/org/bluez/hci0", introspection)
    adapter = obj.get_interface("org.bluez.Adapter1")

    await adapter.call_start_discovery()
    print("Scanning for BLE beacons with names starting with 'PicoBeacon'...")

    try:
        # Keep the script running to listen for signals
        await asyncio.Future()
    except KeyboardInterrupt:
        print("Stopping scan...")
        await adapter.call_stop_discovery()

if __name__ == "__main__":
    asyncio.run(scan_ble_beacons())