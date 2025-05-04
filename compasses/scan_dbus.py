import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType
from dbus_next import Variant

async def main():
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

    introspection = await bus.introspect('org.bluez', '/org/bluez/hci0')
    obj = bus.get_proxy_object('org.bluez', '/org/bluez/hci0', introspection)
    adapter = obj.get_interface('org.bluez.Adapter1')

    # Start discovery
    await adapter.call_start_discovery()
    
    def interfaces_added(path, interfaces):
        if 'org.bluez.Device1' in interfaces:
             props = interfaces['org.bluez.Device1']
             name = props.get('Name').value if 'Name' in props else ''
        if name.startswith('PicoBeacon'):
             address = props.get('Address').value
             rssi = props.get('RSSI').value if 'RSSI' in props else 'N/A'
             print(f"Device found: {name} [{address}], RSSI: {rssi}")

    bus.add_message_handler(lambda msg: (
        interfaces_added(msg.body[0], msg.body[1])
        if msg.member == 'InterfacesAdded' else None
    ))

    # Keep the program running
    await asyncio.get_event_loop().create_future()

asyncio.run(main())