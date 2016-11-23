from readin import ControllerInput
import pigpio
import time

"""Class used To Operate Plane"""
class plane():
    # RANGE OF THROTTLE SERVO
    THROTTLE_RANGE = 800
    # RANGE FOR YAW AND PITCH OUT SERVOS
    RANGE = 200
    # MAXIMUM THROTTLE SERVO SETTING
    MAX = 2500 - 400
    # MINIMUM THROTTLE SERVO SETTING
    MIN = 500 + 400
    # GPIO PIN OF PITCH SERVO
    PITCH = 10
    # GPIO PIN OF YAW SERVO
    YAW = 9
    # GPIO PIN OF THROTTLE SERVO
    THROTTLE = 11
    # raspberry pi pigpio object, API used to interface with Raspberry Pi
    rasp_pi = 0
    # I2C Port
    I2C = 2

    """Connect to API, establishes connections to THROTTLE, PITCH, and YAW controls and
    initializes the I2C connection
    """
    def __init__(self):
        self.rasp_pi = pigpio.pi()  # connect to local Pi
        self.rasp_pi.set_mode(self.THROTTLE, pigpio.OUTPUT)  # GPIO 17 as output
        self.rasp_pi.set_mode(self.PITCH, pigpio.OUTPUT)  # GPIO 17 as output
        self.rasp_pi.set_mode(self.YAW, pigpio.OUTPUT)  # GPIO 17 as output
        self.I2C = self.rasp_pi.i2c_open(1, 0x68)

    """Bitshifts two bits and scales the result to return the z accelation
    @param first
        first bit to shift
    @param second
        second bit to shift
    @return z_accel
        z axis acceleration of plane"""
    def getVal(self, first, second):
        val = self.readVal(first, second)
        val = val / 16384.0
        return val

    """Bitshifts two bits and returns the integer value
    @param first
        first bit to shift
    @param second
        second bit to shift
    @returns bit_result
        the shifted bit result"""
    def readVal(self, first, second):
        bit_result = (first << 8) | second
        if bit_result >= 2 ** 15:
            bit_result = bit_result - 2 ** 16 - 1  # bit shift
        return bit_result

    """Accesses an address, shifts a byte array of size {@code count} to an array of values.
    """
    def readBytes(self, address, count, isData):
        bites = []
        (s, z) = self.rasp_pi.i2c_read_i2c_block_data(self.I2C, address, count)
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
            for i in xrange(4):
                print "!"
                pos = self.readBytes(0x3B, 6, 1)
                (z, y, x) = (pos[0], pos[1], pos[2])
                print z
                # self.stableZAccel(z)
                yaw, pitch, throttle, d = a.poll()
                self.yawOut = 1500 + yaw * self.RANGE
                self.pitchOut = 1500 + pitch * self.RANGE
                self.throttleOut = 1000 + throttle * self.THROTTLE_RANGE

                self.updateControls()


                print yaw, pitch, throttle, d


        a.close()

    def updateControls(self):
        self.rasp_pi.set_servo_pulsewidth(self.YAW, int(self.yawOut))
        self.rasp_pi.set_servo_pulsewidth(self.PITCH, int(self.pitchOut))
        self.rasp_pi.set_servo_pulsewidth(self.THROTTLE, int(self.throttleOut))



aero = plane()
aero.test()
