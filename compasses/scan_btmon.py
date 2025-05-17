import subprocess
import re

# constants for distance calculation
A = 17.48043210453444
m = -1.8071351056155527

def parse_btmon_output():
    try:
        # start btmon process
        process = subprocess.Popen(['btmon'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("Scanning for BLE devices with names starting with 'PicoBeacon'...")

        current_event = {}

        while True:
            line = process.stdout.readline()
            if not line:
                break

            line = line.strip()

            # log btmon output
            # print(f"DEBUG: Line: {line}")

            # Detect the start of a new HCI Event
            if line.startswith('> HCI Event:'):
                if 'Name' in current_event and 'RSSI' in current_event:
                    print(f"{current_event['dist']:.2f} m")
                    current_event = {} # reset for new event

            # log current event
            # print(f"DEBUG: Current event: {current_event}")

            # parse relevant fields
            if 'Name (complete):' in line:
                current_event['Name'] = line.split(':', 1)[1].strip()
            elif 'RSSI:' in line:
                rssi_raw = line.split(':', 1)[1].strip()
                rssi_value = re.search(r'-?\d+', rssi_raw)  # Extract numeric RSSI value
                if rssi_value:
                    rssi = int(rssi_value.group())
                    dist = 10 ** ((A - abs(rssi)) / (10 * m)) / 100
                    current_event['RSSI'] = rssi
                    current_event['dist'] = dist

    except KeyboardInterrupt:
        print("Scanning stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    parse_btmon_output()