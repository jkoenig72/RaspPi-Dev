#!/usr/bin/python
import milight
import sys
import time

ipController = "192.168.10.20"
portController = 8899

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print 'Argument 1:', sys.argv[1]
#print 'Argument 2:', sys.argv[2]

controller = milight.MiLight({'host': ipController, 'port': portController}, wait_duration=0) #Create a controller with 0 wait between commands
light = milight.LightBulb(['rgbw', 'white', 'rgb']) #Can specify which types of bulbs to use

if (sys.argv[1]=='on'):
	controller.send(light.on(int(sys.argv[2]))) # Turn on group param1 lights
	time.sleep(.05)
	controller.send(light.on(int(sys.argv[2]))) # Turn on group param1 lights
	time.sleep(.05)
	controller.send(light.on(int(sys.argv[2]))) # Turn on group param1 lights
else:
	controller.send(light.off(int(sys.argv[2]))) # Turn off group param1 lights
	time.sleep(.05)
	controller.send(light.off(int(sys.argv[2]))) # Turn off group param1 lights
	time.sleep(.05)
	controller.send(light.off(int(sys.argv[2]))) # Turn off group param1 lights

sys.exit(0)



