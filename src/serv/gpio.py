###class for gpio pin to use on the beagleBone ubuntu



###todo
# create look-up dictionary for all gpio
# creat logic to prevent from setting wrong modes
# add checks to confirm the writes
# unexport pin after exporting!!!
#		declare something when crashes to unexport
import sys


#global information for GPIO pin names


class GPIO:
    #class variable
    instances = []
    #instance variables
    pin_name =''
    # CloseAll
    #   static method to close every instance of a GPIO object. 
    #   should be used when closing program, to ensure no pins have be left
    #   exported
    @staticmethod
    def close_all():
        for gpio in GPIO.instances:
            gpio.close()
    #   AddInstance
    @staticmethod
    def __add_instance(gpio):
        #check to make sure gpio is a real object
        if(isinstance(gpio,GPIO)):
            GPIO.instances.append(self)
            #add to instances
            
################init#################
    def __init__(self, pin_name,mode,direction):
        #pin_name = gpmc_ad6	mode = 7 direction = out
        ##############to do, create look up table for names.
        
		
        self.pin_name = pin_name
        self.mode = mode
        self.direction = direction

        ###todo: double check if is or not..
        self.is_exported = False #state of exported pin

        self.state = False #state of the output (false = 0 , true =1 )

        ##like above, set up lookup table
        if(self.pin_name == "gpmc_ad6"):
            self.pin_number = 38

        self.mode_path = "/sys/kernel/debug/omap_mux/"+self.pin_name
        self.export_path = "/sys/class/gpio/export"
        self.pin_path = "/sys/class/gpio/gpio"+str(self.pin_number)
        self.direction_path = self.pin_path+"/direction"
        self.value_path = self.pin_path+"/value"

        ##set up pin mode
        try:
            path = self.mode_path
            f = file(path, 'w')
            f.write("%d" % (self.mode)) #mode determines if input or output
        except IOError:
            print "Error : can\'t find file or read data"
        else:
            print "set mode for pin"
            f.close()

        #export pin
		
		##to do: check if already exported, because this looks like it could error
		# - not error though

        #   in from command line in ubuntu you can export the pin by doing
        #               echo pin# > /sys/class/gpio/export  
        #  to unexport:  echo pin# > /sys/class/gpio/unexport 
        # note: if you get IOError: 16, Device or resource busy, it might be
        #   because trying to export the pin if it is already exported
        try:
            d = file(self.export_path, 'w')
            d.write("%d" % (self.pin_number)) #i
        except IOError:
            print "Error: can\'t open export file"
            sys.exit()
        else:
            print 'exported pin' + str(self.pin_number)
            self.is_exported = True
            d.close()

        #set direction
        try:
            path = self.direction_path
            f = file(path,'w')
            f.write(self.direction)
        except IOError:
            print "Error : can\'t set direction"
            sys.exit()
        else:
            f.close()
            print 'set direction: ' + self.direction
        GPIO.instances.append(self)
		
########close################
    def close(self):
        #unexport the pin
        try:
            f = file("/sys/class/gpio/unexport", 'w')
            f.write("%d" % (self.pin_number))
        except IOError:
            print "error: can\'t unexport pin"
            sys.exit()
        else:
            f.close()    
            print "\n unexported pin: "+ str(self.pin_number)
            self.is_exported = False
        GPIO.instances.remove(self)
    

# subclass for output:
#	this class defines how to implement the super class methods
class OutputGPIO(GPIO):
    def __init__(self, pin_name):
        GPIO.__init__(self, pin_name,7,"out")

#########toggle()#################
    #this will toggle the current state of the output pin
    def toggle(self):
        f = file(self.value_path, 'w')
        try:
            if(self.state == True):
                f.write("0")
                self.state = False
            else:
                f.write("1")
                self.state = True
        except IOError:
            print "Error using toggle"
            f.close()
        else:
            f.close()

######writeVal##################    
    def writeVal(self,val):
        #sanitize input
        if(val!="1" | val!="0"):
            print "why are you doing this to me? \n"
            print "default: val = '0' "
            val = "0"

        path = self.value_path
        f = file(path, 'w')
        f.write(val)
        if(val=="0"):
            self.state = False
        else:
            self.state = True
        f.close()

# sublcass for input:
class InputGPIO(GPIO):
    def __init__(self,pin_name):
        GPIO.__init__(self,pin_name,7,"in") #not tested