###class for gpio pin to use on the beagleBone ubuntu



###todo
# create look-up dictionary for all gpio
# creat logic to prevent from setting wrong modes
# add checks to confirm the writes
# unexport pin after exporting!!!
#		declare something when crashes to unexport
import sys

class GPIO:
  def __init__(self, pin_name,mode,direction):
  #pin_name = gpmc_ad6  mode = 7 direction = out
	#to do, create look up table for names.

  #simple hack for the gpio i know i'm using now
    if (pin_name == "gpmc_ad6"):
       	self.pin_number = 38
    self.pin_name = pin_name
    self.mode = mode
    self.direction = direction
    ##set up pin mode
    try:
      path = "/sys/kernel/debug/omap_mux/"+self.pin_name
      print path
      f = file(path, 'w')
      f.write("%d" % (mode))
    except IOError:
   		print "Error : can\'t find file or read data"
    else:
      print "set mode for pin"
      f.close()

    #export pin
    
    ##to do: check if already exported, because this looks like it could error
    #	- not error though
    try:
      d = file("/sys/class/gpio/export", 'w')
      d.write("%d" % (self.pin_number))
    except IOError:
      print "Error: can\'t open export file"
      sys.exit()
    else:
      print 'exported pin'
      d.close()

     	#set direction
    print str(self.pin_number)
    try:
      path = "/sys/class/gpio/gpio"+str(self.pin_number)+"/direction"
      print path 
      f = file(path,'w')
      f.write(self.direction)
    except IOError:
      print "Error : can\'t set direction"
      sys.exit()
    else:
      f.close()
      print 'set direction'