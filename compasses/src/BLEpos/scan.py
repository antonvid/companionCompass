# import modules
print('importing modules...')
import subprocess
import joblib
import pandas as pd
import numpy as np
from importlib import resources as impresources
import BLEpos.models as modelsDir
import BLEpos.cli as cliDir

cli_filename = 'scanner_AD'

# get space id so we can load the ML model
spaceId = input('enter id for space: ')

model_file = impresources.files(modelsDir) / f"{spaceId}.joblib"
cli = impresources.files(cliDir) / cli_filename

print('loading model ...')
model = joblib.load(model_file)

# initiate rssi data 
data = {
        '11': [],
        '12': [],
        '13': []
}

while True:

    # start cli scanner
    process = subprocess.Popen(
            ["sudo",str(cli)],
            stdout=subprocess.PIPE,
            text=True
    )
    
    # for each beacon ad the scanner receives, parse the data
    for line in process.stdout:
        line_vals = line.split()
        beacon = line_vals[0] + line_vals[1] # get beacon id
        rssi = int(line_vals[2])
    
        data[beacon].append(rssi)

        if len(data[beacon]) > 20: # max rssi values
            data[beacon].pop(0)
    
    # aggregate rssi data into statistics for each beacon
    data_agg = {
            'mean_11':  np.mean(data['11']),
            'std_11':   np.std(data['11']),
            'min_11':   np.min(data['11']),
            'max_11':   np.max(data['11']),
            'mean_12':  np.mean(data['12']),
            'std_12':   np.std(data['12']),
            'min_12':   np.min(data['12']),
            'max_12':   np.max(data['12']),
            'mean_13':  np.mean(data['13']),
            'std_13':   np.std(data['13']),
            'min_13':   np.min(data['13']),
            'max_13':   np.max(data['13']),
    }
    
    # convert this data to a Pandas DataFrame
    live_data = pd.DataFrame([data_agg])
    
    # use the loaded model to predict the location
    prediction = model.predict(live_data)
    print(prediction)

    exit_codes = process.wait()


