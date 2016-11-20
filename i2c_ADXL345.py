#!/usr/bin/env python

# i2c_ADXL345.py
# 2015-04-01
# Public Domain
import binascii
import time
import struct
import sys

import pigpio  # http://abyz.co.uk/rpi/pigpio/python.html

pi = pigpio.pi()  # open local Pi
ADXL345_I2C_ADDR = 0x68

RUNTIME = 60.0

h = pi.i2c_open(1, ADXL345_I2C_ADDR)


"""Gets Value from two indexes of bit array
@param first
    bit[0]
@param second
    bit[1]
"""
def getVal(first, second):
    print first
    print second
    val = (first << 8)| second
    if val >= 2 ** 15:
        val = val - 2 ** 16 - 1  # bit shi
    val = val / 16384.0
    print "WORK"
    return val

def writeByte(address, hval):
    pi.i2c_write_byte_data(h, address, hval)  # wake up mpu6050

def readBytes(address, count):
    bites = []
    (s,z) = pi.i2c_read_i2c_block_data(h, address, count)
    index = 0
    for x in z:
        print x
    first = 0
    second = 1
    while second < count:
        bites[index] = getVal(z[first], z[second])
        first+=2
        second+=2
    return bites

def main():
    if h >= 0:  # Connected OK?
        # Initialise ADXL345.
        pi.i2c_write_byte_data(h, 0x6B, 0)  # wake up mpu6050
        # pi.i2c_write_byte_data(h, 0x2d, 8)  # wake up mpu6050
        # pi.i2c_write_byte_data(h, 0x1C, 0)  # set sensitivity
        pi.i2c_write_byte_data(h, 0xC, 0x10)  # DATA_FORMAT res +/- 2g.

        while True:
            vals = readBytes(0x3B, 2)
            time.sleep(.5)

            print vals

        time.sleep(.2)
    pi.i2c_close(h)

    pi.stop()

main()
