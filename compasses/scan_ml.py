import subprocess
import statistics
import joblib
import pandas as pd

loaded_model = joblib.load('rf_model.joblib')

current = {
        11: None,
        12: None,
        13: None
}

while True:

    process = subprocess.Popen(
            ["sudo","./cli/scanner_AD"],
            stdout=subprocess.PIPE,
            text=True
    )

    for line in process.stdout:
        data = line.split()
        beacon = int(data[0] + data[1])
        rssi = abs(int(data[2]))

        current[beacon] = rssi

        if None in current.values():
            continue

        live_data = pd.DataFrame([[current.values()]], columns=['b1', 'b2', 'b3'])
        prediction = loaded_model.predict(live_data)
        print(prediction)

