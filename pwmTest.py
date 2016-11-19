import sys
import time
import pigpio

class motor():

    pause_time = .1
    pi=1

    def __init__(self):
        print "STARTING"
        self.pi = pigpio.pi()  # connect to local Pi
        self.pi.set_mode(17, pigpio.OUTPUT)  # GPIO 17 as output
        print "Set Pins"


    """Sweeos Motors from 1000-2000"""
    def func(self):
        while True:
            for degree in xrange(1000, 2000, 1):
                self.pi.set_servo_pulsewidth(17, degree)
                print degree
            for degree in xrange(2000, 1000, -1):
                self.pi.set_servo_pulsewidth(17, degree)
                print degree




    def main(self):
        self.pi.set_servo_pulsewidth(17, 1500) # centre


a = motor()
a.func()
a.main()

