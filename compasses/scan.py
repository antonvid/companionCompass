import subprocess
import statistics

A = -26.65441032
m = -4.00150462

while True:

    process = subprocess.Popen(
            ["sudo","./cli/scanner2"],
            stdout=subprocess.PIPE,
            text=True
    )

    rssi = []

    for line in process.stdout:
        data = line.split()
        rssi.append(abs(int(data[1])))

    #print(rssi)

    rssi_mean = statistics.fmean(rssi)
    #print(rssi_mean)
    dist = 10 ** ((A - rssi_mean) / (10*m))
    print(dist,'cm')
