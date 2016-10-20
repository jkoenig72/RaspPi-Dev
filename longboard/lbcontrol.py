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
init = 0
s1=0
speed = 1900
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
	#print(newts)
	#print(oldts)
	if ((oldts+0.1<newts) and (hold == 0)):
		speed = speed - 5
		if (speed<=1900):
			speed=1900
		print(speed)
		pi.set_PWM_dutycycle(4, speed)
		oldts=newts
#defs

def blinkwait():
	pi.write(2, 1)
	sleep(0.125)
	pi.write(2, 0)
	sleep(0.125)

def blinkok():
	pi.write(2, 1)
	sleep(1)
	pi.write(2, 0)
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
			pi.set_PWM_range(4, 2000)
		for event in dev.read_loop():
			#Buttons
			if event.code==164:
				 print("Button 1")
			if (event.code==208 and event.value==1):
				 print("Button 2")
				 if s1==0:
					pi.write(2, 1)
					s1=1
				 else:
					pi.write(2, 0)
					s1=0
				 sleep(0.1)	
			if event.code==1:
				 print("Button 3")
			if event.code==28:
				 print("Button 4")
			if event.code==168:
			 print("Button 5")
			#Joystick
			if event.code==115:
				 #print("UP")
			 	 print(speed)	
				 speed = speed +1
				 if speed >=1999:
					speed=1999	
				 pi.set_PWM_dutycycle(4, speed)	
			if event.code==114:
				 #print("DOWN")
			 	 print(speed)	
				 speed = speed -1
				 if speed <=1900:
					speed=1900	
				 pi.set_PWM_dutycycle(4, speed)	
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
				 print("Tempomat: OFF")
				 hold=0	
			#print(categorize(event))
			#print(event.value)
			#print(event.code)
			#print(event.type)

	except (IOError, OSError):
		print("IO Error... let's try again")
		init = 0
	blinkwait()
	
	
	#print(categorize(event))
	#print(event.value)
	#print(event.code)
	#print(event.type)