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
  5. You can now quit the Thonny app, disconnect the Pico and plug it back in to test it works. Once powered, the Pico's LED should flash quickly, signifiying it is advertising!
    
### Set up tracker
  1. Extensive instructions on how to setup a Raspberry Pi can be found here: https://www.raspberrypi.com/documentation/computers/getting-started.html
     I would recommend doing a 'headless' setup, meaning the Pi doesn't need a keyboard, mouse or monitor to operate
     Make sure you have a method to ssh into the Pi, WiFi is very simple to configure, but you can also look into USB gadget mode so you don't have to worry about having access to WiFi
  2. Once your Pi is set up with an os and you are ssh'd into it, you should run `sudo apt update` and `sudo apt upgrade` to insure everything is up to date, and run `sudo apt install python3-pip`
     to install the python package installer. We use this instead of `apt` as i
  4. Clone the repo to the Pi
  5. Create a Python virtual environment, this will allow us to install the most recent versions of packages, rather than using apt
     `python -m venv ~/env`
  6. Activate the virtual environment using `source ~/env/bin/activate`
  
</ol>

</ol>
