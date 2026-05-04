import subprocess
import csv
import os

filepath = "../data/rssi_coord.csv"

file_exists = os.path.isfile(filepath)

x = int(input("enter x co-ordinate: "))
y = int(input("enter y co-ordinate: "))
n = int(input("enter number of scans: "))

current = {
        11: None,
        12: None,
        13: None
}

with open(filepath, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    if not file_exists:
        writer.writerow(["x", "y", "b1", "b2", "b3"])

    for i in range(n):
        
        process = subprocess.Popen(
                ["sudo","../cli/scanner_AD"],
                stdout=subprocess.PIPE,
                text=True
        )

        for line in process.stdout:
            data = line.split()
            beacon_id = int(data[0]+data[1])
            rssi = data[2]

            current[beacon_id] = rssi;

            print(current)

            if None in current.values():
                continue

            writer.writerow([x, y, current[11], current[12], current[13]])
       
        print(f"{i+1}/{n}")
        exit_code = process.wait()
