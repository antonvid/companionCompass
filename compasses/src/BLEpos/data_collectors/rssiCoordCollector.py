# import modules
import subprocess
import csv
import os
from importlib import resources as impresources
import BLEpos.data as dataDir
import BLEpos.cli as cliDir

scanner_filename = "scanner_AD" # define which cli scannner we are using

cli = impresources.files(cliDir) / scanner_filename # get cli scanner

# data collection function, takes filename and number of scans
def collect(filename, n_scan):

    file = impresources.files(dataDir) / f"{filename}.csv" # get data file

    # check if the data file already exists
    if file.exists():
        print(f"storing data to data/{filename}.csv!")
        file_exists = True
    else:
        print(f"creating file data/{filename}.csv to store data!")
        file_exists = False

    with open(file, 'a', newline='') as csvfile: # open data file
        writer = csv.writer(csvfile)

        # if data file is new, write headers
        if not file_exists:
            writer.writerow(["x", "y", "11", "12", "13"])
        
        # repeats indefinitly until keyboard interrupt, unless user specifies 0 scans
        while n_scan:

            try:
                print("press Ctrl+C if you have finished, else:")
                # get current coords
                x = int(input("enter x co-ordinate: "))
                y = int(input("enter y co-ordinate: "))
            except KeyboardInterrupt:
                print('goodbye')
                break
            
            # initiate/clear rssi data for each beacon
            current = {
                    11: None,
                    12: None,
                    13: None
            }

            for i in range(n_scan): # for number of scans 
                
                # run CLI scanner
                process = subprocess.Popen(
                        ["sudo", str(cli)],
                        stdout=subprocess.PIPE,
                        text=True
                )

                for line in process.stdout:
                    # parse data
                    data = line.split() # split output by ' '
                    beacon_id = int(data[0]+data[1]) # beacon id is defined by beacon's minor and major variable
                    rssi = data[2]

                    if rssi: 
                        current[beacon_id] = rssi
                    
                    # if not got a value for all beacons then don't record to CSV
                    # since we want continuous data
                    if None in current.values():
                        continue
                    
                    # write data!
                    writer.writerow([x, y, current[11], current[12], current[13]])
                    print([x, y, current[11], current[12], current[13]])  

                print(f"scan {i+1}/{n_scan}")
                exit_code = process.wait() # wait until CLI scan is finished before running again

# if file ran as script:
if __name__ == "__main__":

    print("RSSI to coordinate data collector!")

    # ask user for file name and number of scans
    
    print("this data will be stored to ../data/[name].csv")
    filename = str(input("[name] = "))
    filepath = f"../data/{filename}.csv"
    
    print(f"this data collector is using the {scan_filepath} CLI scanner")
    print("for each coordinate, it will run this [n] times")
    n = int(input("[n] = "))

    collect(filepath, n) # run data collection function
