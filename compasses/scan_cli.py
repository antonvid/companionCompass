import subprocess
import csv

dist = input("enter distance to beacon: ")

with open('data.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    for i in range(4):
        
        process = subprocess.Popen(
                ["sudo","./cli/scanner2"],
                stdout=subprocess.PIPE,
                text=True
        )

        for line in process.stdout:
            data = line.split()
            writer.writerow([dist, data[1]])
