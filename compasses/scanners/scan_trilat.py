import subprocess
import statistics

a = -26.65441032
m = -4.00150462

beacons = {}
beacons_rolavg = {}
n = 40
rssi_rolavg = 0

def getPos(beacons):
    beacons_x = []
    beacons_y = []
    beacons_d = []

    for (x, y) in beacons:
        beacons_x.append(x)
        beacons_y.append(y)
        beacons_d.append(beacons[(x, y)])

    if len(beacons_x) < 3:
        return 0,0

    x1 = beacons_x[0]
    x2 = beacons_x[1]
    x3 = beacons_x[2]

    y1 = beacons_y[0]
    y2 = beacons_y[1]
    y3 = beacons_y[2]

    r1 = 10 ** ((a + beacons_d[0]) / (10 * m))
    r2 = 10 ** ((a + beacons_d[1]) / (10 * m))
    r3 = 10 ** ((a + beacons_d[2]) / (10 * m))
    
    print(x1,y1,r1)
   
    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E) 

    return x,y

while True:

    process = subprocess.Popen(
            ["sudo","./cli/scanner_AD"],
            stdout=subprocess.PIPE,
            text=True
    )

    for line in process.stdout:
        data = line.split()
        x = int(data[0])
        y = int(data[1])
        rssi = int(data[2])

        if (x, y) in beacons:
            beacons[(x, y)].append(rssi)
        else:
            beacons[(x, y)] = [rssi]

        if len(beacons[(x, y)]) > n:
            beacons[(x, y)].pop(0)

        values = beacons.get((x, y))
        if len(values) == n:
            beacons_rolavg[(x, y)] = beacons_rolavg[(x,y)] + ((beacons[(x,y)][-1] - beacons[(x,y)][-n]) / n)
        else:
            beacons_rolavg[(x,y)] = beacons[(x, y)][-1]
        #print(beacons)
        #print(beacons_rolavg)

        print(getPos(beacons_rolavg))

        #print(f"{round(rssi_rolavg,2)} -> {dist}cm")
