import subprocess
import csv

with open('../data/rssi_time.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)


    for i in range(4):
        
        process = subprocess.Popen(
                ["sudo","../cli/scanner2"],
                stdout=subprocess.PIPE,
                text=True
        )

        for line in process.stdout:
            data = line.split()

            row = [data[0], data[2]]
            print(row)
            writer.writerow(row)

        exit_codes = process.wait()
