from readin import ControllerInput
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
    h = 2

    def __init__(self):
        self.pi = pigpio.pi()  # connect to local Pi
        self.pi.set_mode(self.THROTTLE, pigpio.OUTPUT)  # GPIO 17 as output
        self.pi.set_mode(self.PITCH, pigpio.OUTPUT)  # GPIO 17 as output
        self.pi.set_mode(self.YAW, pigpio.OUTPUT)  # GPIO 17 as output
        self.h = self.pi.i2c_open(1, 0x68)

    def getVal(self,first, second):
        val = self.readVal(first, second)
        val = val / 16384.0
        return val

    def readVal(self,first, second):
        val = (first << 8) | second
        if val >= 2 ** 15:
            val = val - 2 ** 16 - 1  # bit shi
        return val

    def readBytes(self,address, count, isData):
        bites = []
        (s, z) = self.pi.i2c_read_i2c_block_data(self.h, address, count)
        index = 0
        first = 0
        second = 1
        while second < count:
            if isData:
                bites.append(self.getVal(z[first], z[second]))
            else:
                bites.append(self.readVal(z[first], z[second]))
            first += 2
            second += 2
            index += 1
        return bites


    """Adjusts Servo to Degree specified by user"""
    def test(self):
        while True:
            pos = self.readBytes(0x3B, 6, 1)
            (z, y, x) = (pos[0], pos[1], pos[2])
            print z
            self.stableZAccel(z)
            a = ControllerInput()
            print(a.poll())
            # self.stableZAccel(y)
            # self.stableZAccel(x)
            time.sleep(.1)

    def stableXAccel(self, x):
        if (x < 1):
            self.throttleUp()
        elif (x > 1):
            self.throttleDown()

    def stableYAccel(self, y):
        if (y < 1):
            self.throttleUp()
        elif (y > 1):
            self.throttleDown()

    def stableZAccel(self, z):
        if (z < -1):
            self.throttleUp()
        elif (z > -1.3):
            self.throttleDown()

    def throttleUp(self):
        self.pi.set_servo_pulsewidth(self.THROTTLE, self.MAX)

    def throttleDown(self):
        self.pi.set_servo_pulsewidth(self.THROTTLE, self.MIN)

    def pitchUp(self):
        self.pi.set_servo_pulsewidth(self.PITCH, self.MAX)

    def pitchDown(self):
        self.pi.set_servo_pulsewidth(self.PITCH, self.MIN)

    def yawUp(self):
        self.pi.set_servo_pulsewidth(self.YAW, self.MAX)

    def yawDown(self):
        self.pi.set_servo_pulsewidth(self.YAW, self.MIN)


aero = plane()
aero.test