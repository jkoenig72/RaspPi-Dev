#!/usr/bin/python

# 

from evdev import InputDevice, categorize, ecodes
import time
from time import sleep
import pigpio
import syslog
from threading import Timer,Thread,Event

#vars
SERVO = 4 # All gpios are identified as per BCM number. GPIO 4 as per BCM is GPIO 7 as per board on Pi2 but verify it yourself before connecting
LED = 2
pi = pigpio.pi()
pi.set_mode( SERVO , pigpio.OUTPUT) 
pi.set_servo_pulsewidth(SERVO , 800)

init = 0
s1=0
speed = 1040
min_speed = 1450
max_speed = 1800


hold = 0
oldts  = time.time()

class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def trigger():
	global oldts
	global speed
	global hold
	newts = time.time()
	if ((oldts+0.1<newts) and (hold == 0)):
		speed = speed - 10
		if (speed<=min_speed):
			speed=min_speed
		pi.set_servo_pulsewidth(SERVO , speed)
		oldts=newts
	print("Thread speed: %d" % speed)
#defs

def blinkwait():
	pi.write(LED , 1)
	sleep(0.125)
	pi.write(LED , 0)
	sleep(0.125)

def blinkok():
	pi.write(LED , 1)
	sleep(1)
	pi.write(LED , 0)
	sleep(1)
t = perpetualTimer(0.5,trigger)
t.start()

while 1:
	
	try:
		newts = time.time()
		if init == 0:
			dev = InputDevice('/dev/input/event0')
			print(dev)
			init = 1
			blinkok()	
			print("Init OK")

		for event in dev.read_loop():
			#Buttons
			if event.code==164:
				 print("Button 1")
			if (event.code==208 and event.value==1):
				 print("Button 2")
				 if s1==0:
					pi.write(LED , 1)
					s1=1
				 else:
					pi.write(LED , 0)
					s1=0
				 sleep(0.1)	
			if event.code==1:
				 print("Button 3")
			if event.code==28:
				 print("Button 4")
			if event.code==168:
			 print("Button 5")
			

			#Joystick
			if ((event.code==115) and ((event.value==1) or (event.value==2))):
				 #print("UP")
				 hold=1
			 	 print(speed)	
				 speed = speed + 3
				 if speed >=max_speed:
					speed=max_speed	
				 pi.set_servo_pulsewidth(SERVO , speed)
			
			if (event.code==115) and ((event.value==0)):
				 hold=0
			
			if ((event.code==114) and ((event.value==1) or (event.value==2))):
				 #print("DOWN")
			 	 print(speed)
				 hold=1		
				 speed = speed - 9
				 if speed <=min_speed:
					speed=min_speed	
				 pi.set_servo_pulsewidth(SERVO , speed)
			
			if (event.code==114) and ((event.value==0)):
				 hold=0	
			
			if ((event.code==163) and ((event.value==1) or (event.value==2))):
				 #print("RIGHT")
				 print("Tempomat: ON")
				 hold=1	
			
			if ((event.code==163) and (event.value==0)):
				 #print("RIGHT")
				 print("Tempomat: OFF")
				 hold=0	
			
			if event.code==165:
				 #print("LEFT")
				 print("Tempomat: ON")
				 hold=1	
			print(categorize(event))
			#print(event.value)
			#print(event.code)
			#print(event.type)

		#print("main loop speed: %d" % speed)

	except (IOError, OSError):
		print("IO Error... let's try again")
		init = 0
	blinkwait()
	
	
