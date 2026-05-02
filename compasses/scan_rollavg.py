import subprocess
import statistics

A = -26.65441032
m = -4.00150462

rssi = []
n = 20
rssi_rolavg = 0

while True:

    process = subprocess.Popen(
            ["sudo","./cli/scanner_AD"],
            stdout=subprocess.PIPE,
            text=True
    )

    for line in process.stdout:
        data = line.split()
        rssi.append(abs(int(data[2])))
        
        if len(rssi) > n:
            rssi_rolavg = rssi_rolavg + ( (rssi[-1] - rssi[-n]) / n )
            rssi.pop(0)
        else:
            rssi_rolavg = statistics.mean(rssi)

        dist = int(10 ** ((A - rssi_rolavg) / (10*m)))
        print(rssi)
        print(f"{round(rssi_rolavg,2)} -> {dist}cm")
