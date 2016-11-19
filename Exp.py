import pigpio

"""Adjusts Servo to Degree specified by user"""
def test():
    pi = pigpio.pi()  # connect to local Pi
    pi.set_mode(17, pigpio.OUTPUT)  # GPIO 17 as output
    while True:
        pi.i2c_open(1,3b)

test();