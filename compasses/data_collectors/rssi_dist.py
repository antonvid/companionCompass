import subprocess
import csv

dist = input("enter distance to beacon: ")
n = int(input("enter number of scans: "))

with open('../data/rssi_dist.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    for i in range(n):
        
        process = subprocess.Popen(
                ["sudo","../cli/scanner2"],
                stdout=subprocess.PIPE,
                text=True
        )

        for line in process.stdout:
            data = line.split()
            writer.writerow([dist, data[2]])
       
        print(f"{i}/{n}")
        exit_code = process.wait()
