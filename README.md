<h1>companionCompass</h1>
This project uses low-cost hardware to create an accurate indoor positioning system. The BLEpos package allows you to easily train and run a RandomForest model to estimate your coordinate for a given 'space'
<h2>Features</h2>
<ul>
  <li>Step-by-step data collection</li>
  <li>RandomForest model training</li>
  <li>Displays an estimate of your location</li>
</ul>
<h2>How to Use</h2>
You will need the following hardware:
<ul>
  <li>At least three <b>Raspberry Pi Pico W</b> to use as beacons</li>
  <li><b>Raspberry Pi Zero 2W</b> to use as a tracker</li>
</ul>
<h3>Steps</h3>
<ol>
  <li>Pull the repositiory to your local machine</li>
  <li>
    <h4>Set up beacons</h4>
    <ol>
      <li>Install Thonny at https://thonny.org/</li>
      <li>While holding down the BOOTSEL button on the Pico connect it to your machine, it should appear as a storage device</li>
      <li>
        Open Thonny, in the bottom right there should be a drop down menu where you can select "Install MicroPython..."
        <img width="1016" height="845" alt="Screenshot 2026-05-22 at 11 50 37 pm" src="https://github.com/user-attachments/assets/bfbfc7d6-e04e-407c-bb45-0b008d636fdf" />
      </li>
      <li>
        Make sure to select the right options, it should look something like this: 
        <img width="972" height="801" alt="Screenshot 2026-05-22 at 11 53 45 pm" src="https://github.com/user-attachments/assets/7c2cdd73-119f-402d-b5f4-752064d0dbda" />
      </li>
      <li>
        Once it has finished you can upload the beacons/main.py script from this repo to the Pico. This will make Pico act as a BLE beacon, sending an advertisement every 100ms!
        Click the 'Open' button on the top left, select "This computer", and find the main.py file in your local repo to open it
        Once it's opened you can save it to the Pico by pressing CMD/CTRL + SHIFT + S on your keyboard, select 'Raspberry Pi Pico', and enter the file name 'main.py' before clicking OK
      </li>
      <li>
        You can now quit the Thonny app, disconnect the Pico and plug it back in to test it works. Once powered, the Pico's LED should flash quickly, signifiying it is advertising!
      </li>
    </ol>
  </li>
</ol>
