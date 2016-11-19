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

    """Sweeps Motors from 1000-2000"""
    def sweepUp(self):
        for degree in xrange(1000, 2000, 1):
            self.pi.set_servo_pulsewidth(17, degree)
            print degree

    """Sweeps Motors from 2000-1000"""
    def sweepDown(self):
        for degree in xrange(2000, 1000, -1):
            self.pi.set_servo_pulsewidth(17, degree)
            print degree

    """Sweeps Motors"""
    def motor_sweep(self):
        while True:
            self.sweepUp()
            self.sweepDown()


    def main(self):
        self.pi.set_servo_pulsewidth(17, 1500) # centre


a = motor()
a.motor_sweep()
a.main()

