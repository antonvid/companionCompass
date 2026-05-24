# companionCompass
This project uses low-cost hardware to create an accurate indoor positioning system. The BLEpos package allows you to easily train and run a RandomForest model to estimate your coordinate for a given 'space'
## Features
- Step-by-step data collection
- RandomForest model training
- Displays an estimate of your location
- Saves data and models which can be later updated with new data
## How to set up
You will need the following hardware:
- At least three Raspberry Pi Pico W to use as beacons
- Raspberry Pi Zero 2W to use as a tracker

### Set up beacons
1. Install Thonny at [thonny.org](https://thonny.org/)
2. While holding down the BOOTSEL button on the Pico connect it to your machine, it should appear as a storage device
3. Open Thonny, in the bottom right there should be a drop down menu where you can select 'Install MicroPython...'
![](https://github.com/user-attachments/assets/bfbfc7d6-e04e-407c-bb45-0b008d636fdf)
3. Select your options, they should look something like this, and click 'Install': 
![](https://github.com/user-attachments/assets/7c2cdd73-119f-402d-b5f4-752064d0dbda)
4. Once it has finished you can upload the beacons/main.py script from this repo to the Pico. This will make Pico act as a BLE beacon, sending an advertisement every 100ms!.
Click the 'Open' button on the top left, select "This computer", and find the main.py file in your local repo to open it
Once it's opened you can save it to the Pico by pressing CMD/CTRL + SHIFT + S on your keyboard, select 'Raspberry Pi Pico', and enter the file name 'main.py' before clicking OK
5. Our beacons are identified by their major and minor values, which are determined within main.py:
    ```python
    def demo(adv_interval):
    beacon = iBeacon(
      ble         = bt.BLE(), 
      uuid        = bytearray((
                      0xa4, 0x95, 0xbb, 0x10, 0xc5, 0xb1, 0x4b, 0x44, 
                      0xb5, 0x12, 0x13, 0x70, 0xf0, 0x2d, 0x74, 0xde
                    )),
      major       = 1,
      minor       = 1,
      tx_power    = -50,
      interval 	 = adv_interval
    )

    beacon.advertise()
    ```
    For this demo to work, you must have 3 beacons running, all with major = 1, but each with a unique minor from 1 to 3. Change these values in the script as needed.
6. You can now quit the Thonny app, disconnect the Pico and plug it back in to test it works. Once powered, the Pico's LED should flash quickly, signifiying it is advertising!
7. Repeat steps 2-6 for each Pico giving us 3 advertising beacons, you should then place these beacons around your space, as spread out as you can

### Set up tracker
1. Extensive instructions on how to setup a Raspberry Pi can be found here: https://www.raspberrypi.com/documentation/computers/getting-started.html
I would recommend doing a 'headless' setup, meaning the Pi doesn't need a keyboard, mouse or monitor to operate.
Make sure you have a method to ssh into the Pi, WiFi is very simple to configure, but you can also look into USB gadget mode so you don't have to worry about having access to WiFi
3. Once your Pi is set up with an os and you are ssh'd into it, you should run `sudo apt update` and `sudo apt upgrade` to insure everything is up to date, and run `sudo apt install python3-pip` 
to install the python package installer.
4. Clone the repo to the Pi
5. Create a Python virtual environment, this will allow us to install the most recent versions of packages, rather than using apt
`python -m venv ~/env`
6. Activate the virtual environment using `source ~/env/bin/activate`
7. `cd` into the repo and run `pip install -r requirements.txt` to install all the required python packages for this project
8. Once that's finished we are now ready to start locating! 

## Using the BLEpos package
This project's main features have been compiled into a user-friendly Python package, allowing you to train a Random Forest model on your space, and then use this model to locate the tracker in real-time.
Before starting, you should have 3 beacons placed around your space and running, and you should be ssh'd into the tracker.
### BLEpos.train
This module allows you to collect data for each coordinate of your space, with as many scans as you specify. Bear in mind this can be a slow process if you choose to take lots of scans (>30)
1. On the tracker, make sure the virtual environment is activated, and `cd` to the folder containing the BLEpos package: `cd path/to/repo/compasses/src`
2. Run the BLEpos.train module: `python -m BLEpos.train`, this will ask for an id for your space and for the number of scans you want to perform per coordinate. The space id is used to store data and ML models so remember it!
3. The data collection will now begin, move to a coordinate in your space, and enter the x and y coord as the script asks for them.
4. The script will scan for as many times as you specified earlier, as the counter shows, it's important not to move the tracker too much as this can effect the data.
5. Once it's finished it will ask again for coordinates, this is your chance to move to another coordinate, enter them, and wait as the script collects the data.
6. Once you have collected all the data you want to you can end the data collection by pressing CTRL + C.
7. The module will then aggregate all this data and train a Random Forest model on it, and it's performance will be measured and shown
8. The module is now finished and will have stored a model for your space that you can now use to estimate the trackers location within that space!

##
