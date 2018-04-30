#Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import ./Adafruit_Python_PCA9685/Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685(0X40)

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

def receive_inputX(degrees_2, degrees_1) :

    R = degrees_2 - degrees_1
    output = 0.24 * R
    if(R > 0) :
	    flag = 12
    else:
	    flag = 475

    pwm.set_pwm(0, 0, flag)
    time.sleep(output)
    pwm.set_pwm(0, 0, 0)
    return "true"

# Move servo on channel 1
#pwm.set_pwm(1, 0, 475)
# 0.1 = 90degrees
# 0.24 = 180 degrees
# 0.39 = 270 degrees
# 0.56 = 360 degrees
#time.sleep(0.24)
#pwm.set_pwm(1, 0, 0)  

#pwm.set_pwm(0, 0, 12)
#set sleep time to below for clocwise turn 
# 0.08 = 90 degrees
# 0.24 = 180 degrees
# 0.39 = 270 degrees 
# 0.56 = 360 degrees
#time.sleep(0.24)
#pwm.set_pwm(0, 0, 0)
