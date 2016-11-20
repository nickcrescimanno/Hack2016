import pigpio
import struct
import sys

"""Adjusts Servo to Degree specified by user"""
def test():
    pi = pigpio.pi()  # connect to local Pi
    pi.set_mode(17, pigpio.OUTPUT)  # GPIO 17 as output
    pi.i2c_open(0, 0x68)
    while True:


test()