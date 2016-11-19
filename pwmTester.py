import pigpio

"""Adjusts Servo to Degree specified by user"""
def test():
    pi = pigpio.pi()  # connect to local Pi
    pi.set_mode(17, pigpio.OUTPUT)  # GPIO 17 as output
    pi.set_servo_pulsewidth(17, 1000)
    while True:
        degree = input('DEGREE: ')
        pi.set_servo_pulsewidth(17, degree)

test();