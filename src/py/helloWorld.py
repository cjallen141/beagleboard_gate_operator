#!/usr/bin/python
import sys
import gpio

print "Hello, World!"

##initialize everything

pin38 = gpio.GPIO("gpmc_ad6",7,"out")


for pin in gpio.GPIO.instances:
	del pin
	print 'deleted'