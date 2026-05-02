import subprocess
import csv

id = input('enter file id: ')
n = int(input('scan for how many times: '))

with open(f"../data/rssi_{id}.csv", 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    for i in range(n):
        
        process = subprocess.Popen(
                ["sudo","../cli/scanner2"],
                stdout=subprocess.PIPE,
                text=True
        )

        for line in process.stdout:
            data = line.split()

            row = [data[2]]
            print(row)
            writer.writerow(row)

        exit_code = process.wait()

        
