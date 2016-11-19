import sys
import time
import pigpio

class motor():

    pause_time = .01
    PIN=17
    pi=1

    def __init__(self):
        print "STARTING"
        self.pi = pigpio.pi()  # connect to local Pi
        self.pi.set_mode(self.PIN, pigpio.OUTPUT)  # GPIO 17 as output
        print "Set Pins"

    """Sweeps Motors from 1000-2000"""
    def sweepUp(self):
        for degree in xrange(1000, 2000, 1):
            self.pi.set_servo_pulsewidth(self.PIN, degree)
            time.sleep(self.pause_time)
            print degree

    """Sweeps Motors from 2000-1000"""
    def sweepDown(self):
        for degree in xrange(2000, 1000, -1):
            self.pi.set_servo_pulsewidth(self.PIN, degree)
            time.sleep(self.pause_time)
            print degree

    """Sweeps Motors by Alternating <[1000, 2000], [2000,1000]>"""
    def motor_sweep(self):
        while True:
            self.sweepUp()
            self.sweepDown()

a = motor()
a.motor_sweep()


