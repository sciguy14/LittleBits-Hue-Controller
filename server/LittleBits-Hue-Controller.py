#!/usr/bin/python
# -*- coding: utf-8 -*-

# LittleBits Hue Controller by Jeremy Blum
# Copyright 2014 Jeremy Blum, Blum Idea Labs, LLC.
# http://www.jeremyblum.com
# File: LittleBits-Hue-Controller.py
# License: GPL v3 (http://www.gnu.org/licenses/gpl.html)

# Import Libraries
import ConfigParser, argparse, serial, atexit, os, signal, sys, logging, subprocess, time, re
from phue import Bridge
from crontab import CronTab
from serial.tools import list_ports

# Initialize LittleBits Serial Object so we can exit cleanly
littleBits = serial.Serial()

# Read config options
config = ConfigParser.SafeConfigParser(allow_no_value = True)
config_dataset = config.read(os.path.dirname(os.path.abspath(__file__)) + "/config.ini")

# Prevents Exit Traceback
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

# Don't log phue to console
logger = logging.getLogger('phue')
logger.setLevel(logging.ERROR)
logger.propagate = False

# Preconfigured Settings
baud_rate      = '9600'
default_bri    = '254'
default_mood   = '0'
default_tt_sec = '1'
mood0          = '0.4448, 0.4066'
mood1          = '0.5128, 0.4147'
mood2          = '0.6728, 0.3217'
mood3          = '0.3151, 0.3252'
mood4          = '0.4083, 0.5162'
mood5          = '0.6728, 0.3217'
mood6          = '0.2870, 0.1075'
mood7          = '0.1752, 0.0552'
mood8          = '0.5085, 0.2923'
mood9          = '0.4083, 0.5162'

# Main program execution
def main():
    # Parse optional input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--setup', action='store_true', help="Runs setup Mode", required=False)
    args = vars(parser.parse_args())

    # Enter Setup Mode
    if args.has_key('setup') and args['setup']:
        setup()

    # Run in normal continuous mode, waiting for incoming data
    else:
        # Check to see if config file exists
        if not config_dataset:
            print 'Config file not found or empty. Please run with -s argument to generate a config file.'
            exit()
        loop()

# Runs setup mode for this script
def setup():
    # Intro
    print ''
    print 'Welcome to the LittleBits Hue Controller Setup!'
    print 'This program is open source, so feel free to hack it.'
    print '(c) 2014 Jeremy Blum, Blum Idea Labs (www.jeremyblum.com)'

    print ''
    print 'Follow the prompts. If you need to change your setup in the future, just run this script in setup mode again.'
    print 'You can also manually edit the config file that this setup script will generate.'

    # Hue Hub IP Address
    print ''
    print 'We need to be able to communicate with your Hue lighting hub.'
    print 'If it\'s not already, consider setting your hub to a static IP, or a reserved DHCP IP address.'
    valid_IP = False
    hub_found = False
    while not valid_IP or not hub_found:
        ip = raw_input('Enter the IPv4 Address of your hub (ie. 192.168.0.150): ')
        if is_valid_ipv4(ip):
            valid_IP = True
            print 'Now, go press the "connect" button on the top of your hub'
            raw_input('Once you\'ve done that, hit enter.')
            print 'Searching for Hub at ' + ip + '...',
            sys.stdout.flush()
            try:
                bridge = Bridge(ip)
                bridge.connect()
            except:
                print 'Failed!'
                print 'A Hue Bridge could not be found at that address. Try again.'
            else:
                print 'Found!'
                hub_found = True
        else:
            print 'IP Address is invalid.'

    # Light Choice
    print ''
    print 'Now, we need to choose what lights this will control.'
    print 'Go apply power only to the lights you want this to control.'
    print 'Switch off, unplug, or unscrew Hue lights that you DON\'T want to control.'
    raw_input('Press enter once you\'ve done that...')
    print 'Allowing 10 seconds for the hue api to refresh...',
    sys.stdout.flush()
    time.sleep(10)
    print 'Done.'
    light_ids = hue_get_active_light_ids(bridge)
    light_names = hue_get_light_names(bridge, light_ids)
    group_id = hue_get_group_id(bridge, light_ids)
    print 'Great, lighting group ' + str(group_id) + ' has been added.'
    print 'We\'ll be controlling lights with these IDs/Names:'
    for light_id, light_name in zip(light_ids, light_names):
            print 'Light ID: ' + str(light_id) + ' - ' + light_name
    # TODO: Add some error checking (list length zero, for example)

    # Saving Config
    print ''
    print 'Writing setup info to config file...',
    sys.stdout.flush()
    with open(os.path.dirname(os.path.abspath(__file__)) + "/config.ini", 'w') as f:
            write_config_header(f)
            if not config.has_section('LittleBits'): config.add_section('LittleBits')
            if not config.has_option('LittleBits', 'baud_rate'): config.set('LittleBits', 'baud_rate', baud_rate)

            if not config.has_section('PhilipsHue'): config.add_section('PhilipsHue')
            config.set('PhilipsHue', 'bridge_ip', ip)
            config.set('PhilipsHue', 'group_id',  group_id)
            if not config.has_option('PhilipsHue', 'default_bri'):    config.set('PhilipsHue', 'default_bri',    default_bri)
            if not config.has_option('PhilipsHue', 'default_mood'):   config.set('PhilipsHue', 'default_mood',   default_mood)
            if not config.has_option('PhilipsHue', 'default_tt_sec'): config.set('PhilipsHue', 'default_tt_sec', default_tt_sec)

            if not config.has_section('HueMoods'): config.add_section('HueMoods')
            if not config.has_option('HueMoods', '0'): config.set('HueMoods', '0', mood0)
            if not config.has_option('HueMoods', '1'): config.set('HueMoods', '1', mood1)
            if not config.has_option('HueMoods', '2'): config.set('HueMoods', '2', mood2)
            if not config.has_option('HueMoods', '3'): config.set('HueMoods', '3', mood3)
            if not config.has_option('HueMoods', '4'): config.set('HueMoods', '4', mood4)
            if not config.has_option('HueMoods', '5'): config.set('HueMoods', '5', mood5)
            if not config.has_option('HueMoods', '6'): config.set('HueMoods', '6', mood6)
            if not config.has_option('HueMoods', '7'): config.set('HueMoods', '7', mood7)
            if not config.has_option('HueMoods', '8'): config.set('HueMoods', '8', mood8)
            if not config.has_option('HueMoods', '9'): config.set('HueMoods', '9', mood9)

            config.write(f)
    print 'Done!'

    # Make script run at system boot in background
    print ''
    print 'Setting up cron service to launch the service at boot...',
    sys.stdout.flush()
    cron = CronTab(user=True)
    cron.remove_all(comment='littlebits')
    cron_command = os.path.abspath(__file__)
    job = cron.new(command=cron_command,comment='littlebits')
    job.enable()
    job.every_reboot()
    cron.write()
    print 'Done!'

    print ''
    print 'Setup is now complete. The listening service will launch automatically at system boot.'
    print 'You can test it interactively now by running this script without the -s argument.'

                                                                       
# Normal Program Execution:
def loop():        

    # Create Hue Bridge Object
    bridge = Bridge(config.get('PhilipsHue', 'bridge_ip'))

    # Setup Exit Handler to Kill Serial connection on exit
    atexit.register(exit_handler)

    print 'Running in Continuous mode...'
    while True:
        # Automatically Locate and Connect to LittleBits Controller
        alert_once = False
        while not littleBits.isOpen():
            if not alert_once:
                alert_once = True
                print 'Waiting for valid LittleBits controller to be connected via Serial...'
            connect_to_littleBits()
        try:
            trigger = littleBits.readline()
            data = trigger.strip().split(",")
            if data[0] == "on":
                result = hue_control(bridge, config.getint('PhilipsHue', 'group_id'), data[0], int(data[1]), int(data[2])*51)
            elif data[0] == "off":
                result = hue_control(bridge, config.getint('PhilipsHue', 'group_id'), data[0])
            else:
                result = "Malformed Command."
            print result
            littleBits.flush()
        except serial.SerialException:
            littleBits.close()

# Control Hue lights.
# bridge   = bridge object
# group_id = ID of the light group to control
# state    = "on" or "off"
# bri      = brightness (0-255)
# mood     = mood ID (from 0-9)
# tt       = transition time (seconds)
def hue_control(bridge, group_id, state, mood=None, bri=None, tt=None):  
    if state == "on":
        hue_state = True
    elif state == "off":
        hue_state = False

    if mood is None:
        mood = int(config.getint('PhilipsHue', 'default_mood'))
    if bri is None: 
        bri  = int(config.getint('PhilipsHue', 'default_bri'))
    if tt is None:
        tt = int(config.getint('PhilipsHue', 'default_tt_sec'))

    xy = config.get('HueMoods',str(mood))
    xy = xy.split(", ")
    xy[0] = float(xy[0])
    xy[1] = float(xy[1])
            
    command =  {'transitiontime' : tt*10,
                'on'             : hue_state,
                'bri'            : bri,
                'xy'             : xy}

    bridge.set_group(group_id, command)
    result = "Turned lights " + state + "."
    if state == "on":
        result = result + " (Brightess = " + str(bri) + ", Mood = " + str(mood) + ")"
            
    return result

# Returns a list of all the currently connected hue lights
def hue_get_active_light_ids(bridge):
    lights = bridge.get_light_objects('id')
    active_light_ids = []
    for light_id in lights:
        if bridge.get_light(light_id,'reachable'):
            active_light_ids.append(light_id)

    return active_light_ids

# Return list of the light names associated with list of the provided IDs
def hue_get_light_names(bridge, light_ids):
    light_names = []
    for light_id in light_ids:
        light_names.append(bridge.get_light(light_id, 'name'))

    return light_names

# Checks if "LittleBits Lights" group already exists, and deletes and remakes it with the provided light IDs
# Makes new group if one doesn't exist
# Returns ID of group
def hue_get_group_id(bridge, light_ids):
    GROUP_NAME = "LittleBits Lights"

    #Delete any groups with this name
    group_id = bridge.get_group_id_by_name(GROUP_NAME)
    while group_id:
        bridge.delete_group(group_id)
        group_id = bridge.get_group_id_by_name(GROUP_NAME)

    #Create a new group with the desired lights
    bridge.create_group(GROUP_NAME, light_ids)
    return bridge.get_group_id_by_name(GROUP_NAME)

# Determine the dev location of the LittleBits Hue Controller
# Leaves correct device open in global littleBits serial object
def connect_to_littleBits():
    IDENTIFIER = "LittleBits-Hue-Controller"
    dev_list = list_ports.comports()
    connected = False
    for dev in dev_list:
        try:
            # In the event at that we try to open while the OS is still registering the new port, we'll have issues
            littleBits.baudrate = config.getint('LittleBits', 'baud_rate')
            littleBits.port     = dev[0]
            littleBits.timeout  = .5 #Allow 500ms for response
            littleBits.open()
            littleBits.write('?') # Ask device to identify itself
            reply = littleBits.readline()
        except:
            littleBits.close()
            time.sleep(.5)
        else:
            if reply.rstrip() != IDENTIFIER:
                littleBits.close()
            else:
                print "Connected to LittleBits on " + dev[0]
                connected = True
        if connected:
            littleBits.flush()
            littleBits.timeout  = None
            break

# Write comment header to config file (pass file handle)
# Assumes empty file
def write_config_header(f):
    f.write('# LittleBits Hue Controller by Jeremy Blum\n')
    f.write('# Copyright 2014 Jeremy Blum, Blum Idea Labs, LLC.\n')
    f.write('# http://www.jeremyblum.com\n')
    f.write('# File: config.ini\n')
    f.write('# License: GPL v3 (http://www.gnu.org/licenses/gpl.html)\n\n')

# Validates IPv4 addresses
# http://stackoverflow.com/a/319293
def is_valid_ipv4(ip):
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None

# Closes the serial stream when the program exits
def exit_handler():
    littleBits.close()
    print '\nApplication Terminated. Serial Connection Closed.'

# Run the Main funtion when this python script is executed
if __name__ == '__main__':
    main()
