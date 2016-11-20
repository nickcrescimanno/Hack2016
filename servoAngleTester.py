import pigpio

PITCH = 10
YAW = 9
THROTTLE = 11


"""Adjusts Servo to Degree specified by user"""
def test():
    pi = pigpio.pi()  # connect to local Pi
    pi.set_mode(17, pigpio.OUTPUT)  # GPIO 17 as output
    degree = input('DEGREE: ')
    while True:
        pi.set_servo_pulsewidth(input("ENTER PIN"), degree)

test();