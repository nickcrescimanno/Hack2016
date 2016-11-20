#!/usr/bin/env python

# i2c_ADXL345.py
# 2015-04-01
# Public Domain
import binascii
import time
import struct
import sys

import pigpio  # http://abyz.co.uk/rpi/pigpio/python.html

if sys.version > '3':
    buffer = memoryview

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

        time.sleep(.5)

        if s >= 0:
            # print binascii.hexlify(b)
            (z) = struct.unpack('h', buffer(b))
            # (x, y, z, q, w) = (float (x)/16384.0, float (y)/16384.0, float (z/16384.0), float (q/16384.0), float (w/16384.0))
            # print("x: {} y: {} z: {}? {}? {}? ".format(x, y, z, q, w))
            print("z:{}".format(z))

        else:
            print "WE GOT AN ERROR"
        a=(b[0] <<8)  +  b[1]
        print type(a)
        print a
        time.sleep(.2)
        print a[0]
pi.i2c_close(h)

pi.stop()
