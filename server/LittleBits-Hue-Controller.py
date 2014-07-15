#!/usr/bin/python
# -*- coding: utf-8 -*-

# LittleBits Hue Controller by Jeremy Blum
# Copyright 2014 Jeremy Blum, Blum Idea Labs, LLC.
# http://www.jeremyblum.com
# File: LittleBits-Hue-Controller.py
# License: GPL v3 (http://www.gnu.org/licenses/gpl.html)

import ConfigParser
import argparse
import serial
import atexit
import os
import signal, sys, logging
from phue import Bridge

#Read config options
config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "/config.ini")        

#Create Serial Instance, but don't open it yet.
littleBits = serial.Serial()

#Prevents Exit Traceback
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

#Don't log phue to console
logger = logging.getLogger('phue')
logger.setLevel(logging.WARNING)
logger.propagate = False

#Main program execution
def main():
        
        
        
        #Parse optional input arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--setup', action='store_true', help="Runs setup Mode", required=False)
        args = vars(parser.parse_args())

        #Enter Setup Mode
        if args.has_key('setup') and args['setup']:
                pass #TODO

        #Run in normal continuous mode, waiting for incoming data
        else:
                littleBits.baudrate = config.getint('LittleBits', 'baud_rate')
                littleBits.port     = config.get('LittleBits', 'dev')
                littleBits.open()

                atexit.register(exit_handler)
                print 'Running in Continuous mode...'
                while True:
                    trigger = littleBits.readline()
                    data = trigger.strip().split(",")
                    if data[0] == "on":
                        result = hue(data[0],int(data[1]),int(data[2])*51)
                    elif data[0] == "off":
                        result = hue(data[0])
                    else:
                        result = "Malformed Command."
                    print result
                    littleBits.flush()

def exit_handler():
    littleBits.close()
    print '\nApplication Terminated. Serial Connection Closed.'

#Control Hue lights.
#Allowed state values: "on" "off"
#bri  = brightness (0-255)
#mood = mood ID (from 0-9)
#tt   = transition time (seconds)
def hue(state, mood=int(config.getint('PhilipsHue', 'default_mood')), bri=int(config.getint('PhilipsHue', 'default_bri')), tt=int(config.getint('PhilipsHue', 'default_tt_sec'))):
        
	lights_list =[[x for x in ss.split(', ')] for ss in config.get('PhilipsHue','lights').split('\n')]
	light_ids = map(int, [row[0] for row in lights_list])
	light_names = [row[1] for row in lights_list]
	if len(light_ids) > 0:
		b = Bridge(config.get('PhilipsHue', 'bridge_ip'))
		#b.get_api()   
		if state == "on":
			hue_state = True
		elif state == "off":
			hue_state = False

                xy = config.get('HueMoods',str(mood))
                xy = xy.split(", ")
                xy[0] = float(xy[0])
                xy[1] = float(xy[1])
                
		command =  {'transitiontime' : tt*10,
                            'on'             : hue_state,
                            'bri'            : bri,
                            'xy'             : xy}

		b.set_group(config.getint('PhilipsHue', 'group_id'), command)
		result = "Turned lights " + state + "."
		if state == "on":
                        result = result + " (Brightess = " + str(bri) + ", Mood = " + str(mood) + ")"
		
	else:
		result = "Lights not specified in config file."
	return result

#Run the Main funtion when this python script is executed
if __name__ == '__main__':
	main()
