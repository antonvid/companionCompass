import subprocess
import os

a=-11.99952951145519
m=-2.6194850599011157
Q=1e-07
R=1e-05

rssi_kalman = []

def toDist(rssi):
    return round((10 ** ((a - rssi) / (10 * m)))/100, 1)

while True:

    process = subprocess.Popen(
            ["sudo","./cli/scanner2"],
            stdout=subprocess.PIPE,
            text=True
    )

    for line in process.stdout:

        data = line.split()
        rssi = abs(int(data[2]))
       

        if not rssi_kalman: # Check if the list is empty for initialization
            # Initialize state for the first data point
            X_est = rssi
            P = 1.0 # Initial uncertainty
        else:
            # Prediction step
            # X_est is the previous state estimate, P is the previous error covariance
            X_est_prev = rssi_kalman[-1][0]
            P_prev = rssi_kalman[-1][1]

            # Predict next state (assuming a constant state model: x_t = x_{t-1})
            X_est_pred = X_est_prev
            # Predict next error covariance
            P_pred = P_prev + Q

            # Update step (with current measurement)
            K = P_pred / (P_pred + R) # Kalman gain
            X_est = X_est_pred + K * (rssi - X_est_pred) # Updated state estimate
            P = (1 - K) * P_pred # Updated error covariance

            rssi_kalman.pop(0)
        
        rssi_kalman.append([X_est, P]) # Append the current estimated state and its covariance

        #print(rssi_kalman[-1][0])
    
    os.system('clear')
    dist = toDist(rssi_kalman[-1][0])

    print(f'{dist}m')
    
    exit_code = process.wait()

        
