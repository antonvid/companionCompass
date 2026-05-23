# companionCompass
This project uses low-cost hardware to create an accurate indoor positioning system. The BLEpos package allows you to easily train and run a RandomForest model to estimate your coordinate for a given 'space'
## Features
- Step-by-step data collection
- RandomForest model training
- Displays an estimate of your location
## How to Use
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
7. Repeat steps 2-6 for each Pico giving us 3 advertising beacons

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
