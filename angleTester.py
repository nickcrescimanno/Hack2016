import pigpio


def test():
    pi = pigpio.pi()  # connect to local Pi
    pi.set_mode(17, pigpio.OUTPUT)  # GPIO 17 as output
    while True:
        degree = input('DEGREE: ')
        pi.set_servo_pulsewidth(17, degree)

test();