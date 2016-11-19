import sys
import time

import pigpio

<<<<<<< HEAD
pi = pigpio.pi() # connect to local Pi
pi.set_mode(17, pigpio.OUTPUT) # GPIO 17 as output
#pi.set_servo_pulsewidth(17, 1500) # centre
pi.set_servo_pulsewidth(17, 0)    # off
=======
def main():
    pi = pigpio.pi() # connect to local Pi
    pi.set_mode(17, pigpio.OUTPUT) # GPIO 17 as output
    pi.set_servo_pulsewidth(17, 1500) # centre

main()
>>>>>>> ff8c74abaf222f65cea608e555a931d22a2154aa
