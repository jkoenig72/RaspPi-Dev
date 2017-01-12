#!/usr/bin/python
from evdev import InputDevice, categorize, ecodes
import time
from time import sleep
import pigpio
import syslog
from threading import Timer,Thread,Event

#vars
SERVO = 4 # All gpios are identified as per BCM number. GPIO 4 as per BCM is GPIO 7 as per board on Pi2 but verify it yourself before connecting

pi = pigpio.pi() # Connect to local Pi.
pi.set_mode( SERVO , pigpio.OUTPUT) 
pi.set_servo_pulsewidth(SERVO , 800)
