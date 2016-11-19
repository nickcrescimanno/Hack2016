import sys
import time

import pigpio

pi = pigpio.pi() # connect to local Pi
pi.set_mode(17, pigpio.OUTPUT) # GPIO 17 as output
pi.set_servo_pulsewidth(17, 1500) # centre
