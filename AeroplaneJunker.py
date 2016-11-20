from readin import ControllerInput
import pigpio
import time


class plane():
    THROTTLE_RANGE = 800
    RANGE = 200
    MAX = 2500 - 400
    AVG = 1500
    MIN = 500 + 400
    PITCH = 10
    YAW = 9
    THROTTLE = 11
    pi = 0
    h = 2
    YAW_CENTER = 1500
    PITCH_CENTER = 1500

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
        notPressed = True
        a = ControllerInput()
        while True:
            for i in xrange(4):
                print "!"
                pos = self.readBytes(0x3B, 6, 1)
                (z, y, x) = (pos[0], pos[1], pos[2])
                print z
                # self.stableZAccel(z)
                yaw, pitch, throttle, d = a.poll()
                if d!=0 and dOld==0:
                    for i in range(7):
                        if (d & 2**i) != 0:
                            self.trim(i)
                dOld = d

                self.yawOut = self.YAW_CENTER - yaw * self.RANGE
                self.pitchOut = self.PITCH_CENTER - pitch * self.RANGE
                self.throttleOut = 1000 + throttle * self.THROTTLE_RANGE

                self.updateControls()

                print yaw, pitch, throttle, d

        a.close()

    def trim(self, button):
        if button==4:
            self.PITCH_CENTER-=50
        if button==5:
            self.PITCH_CENTER += 50
        if button == 6:
            self.YAW_CENTER -= 50
        if button == 7:
            self.YAW_CENTER += 50

    def updateControls(self):
        self.pi.set_servo_pulsewidth(self.YAW, int(self.yawOut))
        self.pi.set_servo_pulsewidth(self.PITCH, int(self.pitchOut))
        self.pi.set_servo_pulsewidth(self.THROTTLE, int(self.throttleOut))

    def smooth(self, yaw, pitch, throttle):


aero = plane()
aero.test()