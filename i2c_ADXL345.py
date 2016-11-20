#!/usr/bin/env python

# i2c_ADXL345.py
# 2015-04-01
# Public Domain
import binascii
import time
import struct
import sys

import pigpio  # http://abyz.co.uk/rpi/pigpio/python.html

"""Gets Value from two indexes of bit array
@param first
    bit[0]
@param second
    bit[1]
"""
def getVal(first, second):
    val = (first << 8) + second
    if val >= 2 ** 15:
        val = val - 2 ** 16 - 1  # bit shi
    val = val / 16384.0
    return val

def main():
    BUS = 1

    ADXL345_I2C_ADDR = 0x68

    RUNTIME = 60.0

    pi = pigpio.pi()  # open local Pi

    h = pi.i2c_open(BUS, ADXL345_I2C_ADDR)

    if h >= 0:  # Connected OK?

        # Initialise ADXL345.
        pi.i2c_write_byte_data(h, 0x6B, 0)  # wake up mpu6050
        # pi.i2c_write_byte_data(h, 0x2d, 8)  # wake up mpu6050
        # pi.i2c_write_byte_data(h, 0x1C, 0)  # set sensitivity
        pi.i2c_write_byte_data(h, 0xC, 0x10)  # DATA_FORMAT res +/- 2g.

        (s, b) = pi.i2c_read_i2c_block_data(h, 0x1C, 1)
        print binascii.hexlify(bytearray(b))

        while True:
            (s, b) = pi.i2c_read_i2c_block_data(h, 0x3F, 2)
            if s < 0:
                print "WE GOT AN ERROR"
            time.sleep(.5)

            a = getVal(b[0], b[1])
            print a

        time.sleep(.2)
    pi.i2c_close(h)

    pi.stop()

main()
