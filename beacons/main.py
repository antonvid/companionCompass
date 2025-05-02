from machine import Pin
from time import sleep
import bluetooth
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x03)

FLAG_GENERAL_DISC_MODE = const(0x02)
FLAG_LE_ONLY = const(0x04)

# Onboard LED pin (GP25)
led = machine.Pin("LED", machine.Pin.OUT)

class BLEBeacon:
    def __init__(self, name):
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)

        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            print("Central connected")
        elif event == _IRQ_CENTRAL_DISCONNECT:
            print("Central disconnected")
            self._advertise()  # Start advertising again after disconnect

    def _advertise(self):
        name_bytes = bytes(self.name, 'utf-8')
        adv_data = bytearray()
        adv_data += bytearray((len(name_bytes) + 1, _ADV_TYPE_NAME)) + name_bytes
        adv_data += bytearray((2, _ADV_TYPE_FLAGS, FLAG_GENERAL_DISC_MODE | FLAG_LE_ONLY))

        self.ble.gap_advertise(100, adv_data)

def main():
    beacon = BLEBeacon("PicoBeacon1")
    while True:
        led.toggle
        sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        led.value(0)