import subprocess
import statistics
import joblib
import pandas as pd

rf = joblib.load('rf_model.joblib')
print("loaded random forest model!")

Q = 0.1
R = 100

kalman = {
        '11': [],
        '12': [],
        '13': []
}

while True:
    
    process = subprocess.Popen(
            ["sudo","./cli/scanner_AD"],
            stdout=subprocess.PIPE,
            text=True
    )

    for line in process.stdout:
        data = line.split()
        beacon = data[0] + data[1]
        rssi = int(data[2])

        if not kalman[beacon]:
            X_est = rssi
            P = 1.0
        else:
            X_est_prev = kalman[beacon][-1][0]
            P_prev = kalman[beacon][-1][1]

            X_est_pred = X_est_prev
            P_pred = P_prev + Q

            K = P_pred / (P_pred + R)
            X_est = X_est_pred + K * (rssi - X_est_pred)

            P = (1 - K) * P_pred

            kalman[beacon].pop(0)

        kalman[beacon].append([X_est, P])

    current = {b: int(r[0][0]) for b, r in kalman.items()}
    
    live_data = pd.DataFrame([current])
    print(live_data)
    prediction = rf.predict(live_data)
    print(prediction)

    exit_codes = process.wait()

