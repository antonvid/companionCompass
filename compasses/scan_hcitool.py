import asyncio
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# constants for distance calculation
A = 17.48043210453444
m = -1.8071351056155527

def parse_hcitool_output(line):
    """Parse a line of hcitool output to extract device information."""
    parts = line.strip().split(None, 1)
    if len(parts) == 2:
        mac_address, name = parts
        return mac_address, name
    return None, None

async def main():
    try:
        # Start hcitool lescan --duplicates
        process = subprocess.Popen(
            ["hcitool", "lescan", "--duplicates"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        logging.info("Scanning for BLE devices using hcitool... Press Ctrl+C to stop.")

        # Process the output in real-time
        while True:
            line = process.stdout.readline()
            if not line:
                break

            mac_address, name = parse_hcitool_output(line)
            if name and name.startswith("PicoBeacon"):
                # Extract RSSI value from the line (if available)
                rssi = "Unknown"  # Default value if RSSI is not present
                if "RSSI:" in line:
                    try:
                        rssi = int(line.split("RSSI:")[-1].strip())
                    except ValueError:
                        pass

                logging.info(f"{name} | RSSI: {rssi}")

    except KeyboardInterrupt:
        logging.info("Stopping scan...")
        process.terminate()
    except Exception as e:
        logging.error(f"Error during BLE scanning: {e}")
    finally:
        if process.poll() is None:
            process.terminate()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")