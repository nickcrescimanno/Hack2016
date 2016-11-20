from readin import ControllerInput
import pigpio
import time


class plane():
    THROTTLE_RANGE = 800
    RANGE = 50
    MAX = 2500 - 400
    AVG = 1500
    MIN = 500 + 400
    PITCH = 10
    YAW = 9
    THROTTLE = 11
    pi = 0
    h = 2

    def __init__(self):
        self.pi = pigpio.pi()  # connect to local Pi
        self.pi.set_mode(self.THROTTLE, pigpio.OUTPUT)  # GPIO 17 as output
        self.pi.set_mode(self.PITCH, pigpio.OUTPUT)  # GPIO 17 as output
        self.pi.set_mode(self.YAW, pigpio.OUTPUT)  # GPIO 17 as output
        self.h = self.pi.i2c_open(1, 0x68)

    def getVal(self, first, second):
        val = self.readVal(first, second)
        val = val / 16384.0
        return val

    def readVal(self, first, second):
        val = (first << 8) | second
        if val >= 2 ** 15:
            val = val - 2 ** 16 - 1  # bit shi
        return val

    def readBytes(self, address, count, isData):
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
        a = ControllerInput()
        while True:
            print "!"
            pos = self.readBytes(0x3B, 6, 1)
            (z, y, x) = (pos[0], pos[1], pos[2])
            print z
<<<<<<< HEAD
            # self.stableZAccel(z)
=======
            # self.stableZAccel(z)            
>>>>>>> 33dd4f8cd5b8db5a780fbadff56f963cd3493db0
            yaw, pitch, throttle, d = a.poll()
            # self.updateControls(yaw, pitch, throttle)
            print yaw, pitch, throttle, d
            # self.stableZAccel(y)
            # self.stableZAccel(x)
            time.sleep(.1)
        a.close()



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

    def updateControls(self, yaw, pitch, throttle):
        yawOut = 1500 + yaw * self.RANGE
        pitchOut = 1500 + pitch * self.RANGE
        throttleOut = 1000 + throttle * self.THROTTLE_RANGE

        self.pi.set_servo_pulsewidth(self.YAW, int(yawOut))
        self.pi.set_servo_pulsewidth(self.PITCH, int(pitchOut))
        self.pi.set_servo_pulsewidth(self.THROTTLE, int(throttleOut))
        (yawOut, pitchOut, throttleOut) = (yawOut, pitchOut, throttleOut)



aero = plane()
aero.test()
