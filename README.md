LittleBits Hue Controller
=========================
The LittleBits Hue Controller is an easy-to-setup, wall-mountable, physical controller for your Philips Hue lightbulbs. The controller makes it easy to turn the lights on/off, change their brightness, and cycle through preset colors. This is a great project for people who hate having to pull their phone out every time they want to adjust their lights.

Getting Setup
=============
What you'll need
----------------
* Some LittleBits!
    * [Arduino Module](http://www.shareasale.com/r.cfm?B=612266&U=966033&M=53280&urllink=)
	* [Micro USB Power Bit](http://shrsl.com/?~7bfw)
	* [3-way Splitter Bit](http://shrsl.com/?~7bfv)
	* [Bar Graph Bit](http://shrsl.com/?~7bfu)
	* [7-seg Display Bit](http://shrsl.com/?~7bft)
	* [Mounting Board](http://shrsl.com/?~7bfs)
	* [2x Button Bits](http://shrsl.com/?~7bfx)
	* [Dimmer Bit](http://shrsl.com/?~7bfy)
* An always-on Linux Machine. This can be a Raspberry Pi or something similar. These instructions assume a debian-based distro, like Ubuntu or Raspbian.
* A Phillips Hue Hub, and one or more Phillips Hue Bulbs
* Two Micro USB Cables (Right Angle is best)
* A 3D printer (optional, for making the enclosure)
* 4 sets of M3x10 Socket Head Bolts and Nuts (for assembling the enclosure)

3D Print the Enclosure and Assemble the LittleBits
-----------------------
Step 1: Place the Bits on the backer board as shown. Print the button/dial covers. Slightly heat the button/dial covers and press them onto the buttons and covers as shown.
![Step 1](http://www.jeremyblum.com/wp-content/uploads/2014/12/step1.jpg)

Step 2: Print the enclosure. Place the front of the enclosure on the panel as shown.
![Step 2](http://www.jeremyblum.com/wp-content/uploads/2014/12/step2.jpg)

Step 3: Press the four M3 nuts into the four slots on the top cover as shown.
![Step 3](http://www.jeremyblum.com/wp-content/uploads/2014/12/step3.jpg)

Step 4: Place the USB wires into the cutt-out on the rear of the panel as shown.
![Step 4](http://www.jeremyblum.com/wp-content/uploads/2014/12/step4.jpg)

Step 5: Screw the bolts into the nuts and apply a velcro backer as shown.
![Step 5](http://www.jeremyblum.com/wp-content/uploads/2014/12/step5.jpg)

Program the Arduino Bit
-------------------------------
* Provide Power to the controller, and connect the Arduino cable to your computer (workstation computer, not the linux server computer)
* Use the provided Arduino Sketch to program the Arduino Bit via the Arduino IDE (select Arduino Leonardo from the device menu)

Install the Python Prerequisites
--------------------------------
* Log into (locally or via SSH) to the network-connected, always-on linux machine that you'll use (Raspberry Pi is good for this)
* Install Python 2.7 if don't already have it installed: `sudo apt-get install python2.7`
* Install Python PIP if you haven't already: `sudo apt-get install python-dev python-pip`
* Install the PHue Library: `sudo pip install phue`
* Install the PySerial Library: `sudo pip install pyserial`
* Install the CronTab Library: ` sudo pip install python-crontab`

Obtain and Setup the Server Script
----------------------------------
* Stay logged into your network linux machine
* Connect your LittleBits Hue Controller to power, and to a USB port on your linux machine
* On your linux machine, navigate to your home directory, and clone this GitHub repo: `git clone https://github.com/sciguy14/LittleBits-Hue-Controller`
* Navigate to the server script directory: `cd LittleBits-Hue-Controller/server`
* Ensure the script is executable: `chmod 755 LittleBits-Hue-Controller.py`
* Execute the script in setup mode and follow the instructions to automatically setup the system: `./LittleBits-Hue-Controller.py -s`. The output will look something like this:
![Setup Screenshot](http://www.jeremyblum.com/wp-content/uploads/2014/12/setup.png)
* That's it! The handler script will now automatically run in the background at boot. You can launch it immediately to observe its output as you toggle the controller, by running: `./LittleBits-Hue-Controller.py`. The screenshot shows the behavior as I adjust brightness, color, and state via the control pad. You can also see it automatically recover when the control pad is unplugged and plugged back in:
![Usage Screenshot](http://www.jeremyblum.com/wp-content/uploads/2014/12/usage.png

More Info
=========
* [Project Post on my Blog](http://www.jeremyblum.com/2014/12/16/littlebits-hue-lighting-controller)
* [LittleBits Project Page](http://littlebits.cc/projects/littlebits-hue-lighting-controller)
* [Thingiverse Project Page](http://www.thingiverse.com/thing:596186)
* [YouTube Demo Video](https://www.youtube.com/watch?v=p_GHpPhFpdo)

License
=======
This work is licensed under the [GNU GPL v3](http://www.gnu.org/licenses/gpl.html).
Please share improvements or remixes with the community, and attribute me (Jeremy Blum, <http://www.jeremyblum.com>) when reusing portions of my code.


