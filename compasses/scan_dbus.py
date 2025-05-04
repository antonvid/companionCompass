import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import MessageType
from dbus_next import Variant

def parse_device(interface_props):
    name = interface_props.get("Name", Variant("s", "")).value
    address = interface_props.get("Address", Variant("s", "")).value
    rssi = interface_props.get("RSSI", Variant("n", 0)).value
    return name, address, rssi

async def run():
    bus = await MessageBus(system=True).connect()

    # Register signal handler
    def signal_handler(message):
        if message.message_type != MessageType.SIGNAL:
            return
        if message.member != "InterfacesAdded":
            return
        path, interfaces = message.body
        device = interfaces.get("org.bluez.Device1")
        if not device:
            return

        name, address, rssi = parse_device(device)
        if name.startswith("PicoBeacon"):
            print(f"[FOUND] {name} | {address} | RSSI: {rssi}")

    bus.add_message_handler(signal_handler)

    # Get adapter and start discovery
    introspection = await bus.introspect("org.bluez", "/org/bluez/hci0")
    obj = bus.get_proxy_object("org.bluez", "/org/bluez/hci0", introspection)
    adapter = obj.get_interface("org.bluez.Adapter1")

    await adapter.call_start_discovery()

    print("Scanning for PicoBeacon devices...")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping scan...")
        await adapter.call_stop_discovery()

asyncio.run(run())
