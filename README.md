LittleBits Hue Controller
=========================
The LittleBits Hue Controller is an easy-to-setup, wall-mountable, physical controller for your Philips Hue lightbulbs. The controller makes it easy to turn the lights on/off, change their brightness, and cycle through preset colors. This is a great project for people who hate having to pull their phone out every time they want to adjust their lights.

Getting Setup
=============
What you'll need
----------------
* Some LittleBits!
    * Arduino Module
	* Micro USB Power Bit
	* 3-way Splitter Bit
	* Bar Graph Bit
	* 7-seg Display Bit
* An always-on Linux Machine. This can be a Raspberry Pi or something similar. These instructions assume a debian-based distro, like Ubuntu or Raspbian.
* A Phillips Hue Hub, and one or more Phillips Hue Bulbs
* Two Micro USB Cables (Right Angle if you want to use the 3D printed enclosure)
* A 3D printer (optional, for making the enclosure)
* 4 sets of M3x10 Socket Head Bolts and Nuts (for assembling the enclosure)

Assemble the LittleBits
-----------------------
```
										 -> Button ->                          -> 
5V Micro USB Power Bit -> 3 Way Splitter -> Dial   -> Arduino Bit (Analog Out) -> Bar Graph Bit
										 -> Button ->             (Analog Out) -> 7seg Bit (values)
```

3D Print, Assemble, and Program
-------------------------------
* 3D Print the parts
* Route the cables through the routing channels (one to power, and one to Arduino)
* Attach the button and Dial heads (It's helpful to heat them up with a heatgun so they slide on)
* Provide Power to the controller, and connect the Arduino cable to your computer
* Use the provided Arduino Sketch to program the Arduino Bit (select Arduino Leonardo from the device menu)

Install the Python Prerequisites
--------------------------------
* Log into (locally or via SSH) the network-connected, always-on linux machine that you'll use (Raspberry Pi is good for this)
* Install Python 2.7 if don't already have it installed: `sudo apt-get install python2.7`
* Install Python PIP if you haven't already: `sudo apt-get install python-dev python-pip`
* Install the PHue Library: `sudo pip install phue`
* Install the PySerial Library: `sudo pip install pyserial`
* Install the CronTab Library: ` sudo pip install python-crontab`

Obtain and Setup the Server Script
----------------------------------
* Stay logged into your network linux machine
* Connect your LittleBits Hue Controller to power, and to a USB port on your machine
* On your machine, navigate to your home directory, and clone this GitHub repo: `git clone https://github.com/sciguy14/LittleBits-Hue-Controller`
* Navigate to the server script directory: `cd LittleBits-Hue-Controller/server`
* Ensure the script is executable: `chmod 755 LittleBits-Hue-Controller.py`
* Execute the script in setup mode and follow the instructions to automatically setup the system: `./LittleBits-Hue-Controller.py -s`
* That's it! The handler script will now automatically run in the background at boot. You can launch it immediately to observe its output as you toggle the controller, by running: `./LittleBits-Hue-Controller.py`

License
=======
This work is licensed under the [GNU GPL v3](http://www.gnu.org/licenses/gpl.html).
Please share improvements or remixes with the community, and attribute me (Jeremy Blum, <http://www.jeremyblum.com>) when reusing portions of my code.


