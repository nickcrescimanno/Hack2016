import pigpio
import time

class plane():
    MAX=2500-200
    AVG=1500
    MIN=500+200
    PITCH = 10
    YAW = 9
    THROTTLE = 11
    pi=0

    def __init__(self):
        self.pi = pigpio.pi()  # connect to local Pi
        self.pi.set_mode(self.THROTTLE, pigpio.OUTPUT)  # GPIO 17 as output
        self.pi.set_mode(self.PITCH, pigpio.OUTPUT)  # GPIO 17 as output
        self.pi.set_mode(self.YAW, pigpio.OUTPUT)  # GPIO 17 as output

    def getVal(self,first, second):
        val = self.readVal(first, second)
        val = val / 16384.0
        return val

    def readVal(self,first, second):
        val = (first << 8) | second
        if val >= 2 ** 15:
            val = val - 2 ** 16 - 1  # bit shi
        return val

    """Adjusts Servo to Degree specified by user"""
    def test(self):
        while True:
            vals = self.readBytes(0x3B, 6, 1)
            print vals[0], vals[1], vals[2]
            time.sleep(.1)


    def throttleUp(self):
        self.pi.set_servo_pulsewidth(self.THROTTLE, self.MAX)

    def throttleDown(self):
        self.pi.set_servo_pulsewidth(self.THROTTLE, self.MIN)

    def pitchUp(self):
        self.pi.set_servo_pulsewidth(self.PITCH, self.MAX)

    def pitchDown(self):
        self.pi.set_servo_pulsewidth(self.PITCH, self.MIN)

    def yawUp(self):
        self.pi.set_servo_pulsewidth(self.YAWW, self.MAX)

    def yawDown(self):
        self.pi.set_servo_pulsewidth(self.YAW, self.MIN)


aero = plane()
aero.test