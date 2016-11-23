from readin import ControllerInput
import pigpio
import time


class plane():
    # RANGE OF THROTTLE SERVO
    THROTTLE_RANGE = 800
    # CENTER YAW POSITION FOR SERVO
    YAW_CENTER = 1500
    # CENTER PITCH POSITION FOR PITCH
    PITCH_CENTER = 1500
    # RANGE FOR YAW AND PITCH OUT SERVOS
    RANGE = 200
    # MAXIMUM THROTTLE SERVO SETTING
    MAX = 2500 - 400
    # MINIMUM THROTTLE SERVO SETTING
    MIN = 500 + 400
    # degree of pitch set on pwm servo (will change according to user)
    pitch = None
    # degree of throttle set on pwm servo(will change according to user)
    throttle = None
    # degree of yaw set on pwm servo (will change according to user)
    yaw = None
    # GPIO PIN OF PITCH SERVO
    PIN_PITCH = 10
    # GPIO PIN OF YAW SERVO
    PIN_YAW = 9
    # GPIO PIN OF THROTTLE SERVO
    PIN_THROTTLE = 11
    # raspberry pi pigpio object, API used to interface with Raspberry Pi
    rasp_pi = None
    # I2C Port
    I2C = 2
    # I2C Address
    I2C_ADDRESS = 0x68
    # BUS NUMBER
    BUS_NUM = 1

    """Connect to API, establishes connections to THROTTLE, PITCH, and YAW controls and
    initializes the I2C connection.
    """
    def __init__(self):
        self.rasp_pi = pigpio.pi()  # connect to local Pi
        self.rasp_pi.set_mode(self.PIN_THROTTLE, pigpio.OUTPUT)  # GPIO 17 as output
        self.rasp_pi.set_mode(self.PIN_PITCH, pigpio.OUTPUT)  # GPIO 17 as output
        self.rasp_pi.set_mode(self.PIN_YAW, pigpio.OUTPUT)  # GPIO 17 as output
        self.I2C = self.rasp_pi.i2c_open(self.BUS_NUM, self.I2C_ADDRESS)

    """Bit shifts two bits and scales the result to return the z accelation
    @param first
        first bit to shift
    @param second
        second bit to shift
    @return z_accel
        z axis acceleration of plane"""
    def get_z_accel(self, first, second):
        raw_accel = self.readVal(first, second)
        ACCEL_SCALE = 16384.0
        z_accel = raw_accel / ACCEL_SCALE
        return z_accel

    """Bit shifts two bits and returns the integer value
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

    """Reads byte array of size {@code count} and returns an array of the decimal result.
    If {@code isAccelData} is True:
        Then resulting decimal values are scaled to return accurate acceleration
    else:
        Resulting Data is not scaled
        @param address
            address to read block data from
        @param count
            length of resulting decimal array
        @param isData
            boolean of whether byte array contains accelerationData
        @return dec_values
            array of decimal values converted from byte array"""
    def readBytes(self, address, count, isAccelData):
        dec_values = []
        (s, block_data) = self.rasp_pi.i2c_read_i2c_block_data(self.I2C, address, count)
        index = 0
        first = 0
        second = 1
        """
        Crawl Across Adjacent Pairs of block Data array and convert to array of decimal values.
        """
        while second < count:
            if isAccelData:
                dec_values.append(self.get_z_accel(block_data[first], block_data[second]))
            else:
                dec_values.append(self.readVal(block_data[first], block_data[second]))
            first += 2
            second += 2
            index += 1
        return dec_values

    """Flies the plane according to {@code ControllerInput}"""
    def fly(self):
        dOld=0
        controller = ControllerInput()
        while True:
            """Print Acceleration Data"""
            accel_data = self.readBytes(0x3B, 6, 1)
            (z, y, x) = (accel_data[0], accel_data[1], accel_data[2])
            print z
            """Monitor Controller Input"""
            new_yaw, new_pitch, new_throttle, d = controller.poll()
            """Trim if needed"""
            if d!=0 and dOld==0:
                for button in range(7):
                    if (d & 2**button) == 1:
                        self.trim(button)
            dOld = d
            """Update Yaw"""
            self.update_plane_yaw(new_yaw)
            """update Pitch"""
            self.update_plane_pitch(new_pitch)
            self.throttle = 1000 + new_throttle * self.THROTTLE_RANGE
            self.updateControls()

    """Updates Plane's Pitch. If {@code new_pitch} exceeds servo pwm bounds,
    {@code self.pitch} will be set to appropriate bound
    @replaces self.pitch"""
    def update_plane_yaw(self, new_yaw):
        self.yaw = self.YAW_CENTER - new_yaw * self.RANGE
        if (self.MIN > self.yaw):
            self.yaw = self.MIN
        elif (self.MAX < self.yaw):
            self.yaw = self.MAX

    """Updates Plane's Pitch. If {@code new_pitch} exceeds servo pwm bounds,
    {@code self.pitch} will be set to appropriate bound
    @replaces self.pitch"""
    def update_plane_pitch(self,  new_pitch):
        self.pitch = self.PITCH_CENTER - new_pitch * self.RANGE
        if (self.MIN > self.pitch):
            self.pitch = self.MIN
        elif (self.MAX < self.pitch):
            self.pitch = self.MAX

    """Trims pitch and yaw according to {@code button} pressed"""
    def trim(self, button):
        if (button==4):
            self.PITCH_CENTER-=50
        if button==5:
            self.PITCH_CENTER += 50
        if button == 6:
            self.YAW_CENTER -= 50
        if button == 7:
            self.YAW_CENTER += 50
    
    """Updates Yaw, Pitch and Throttle of plane according to {@code self.yaw},
       {@code self.pitch}, and {@code self.throttle}
    @updates self.rasp_pi"""
    def updateControls(self):
        self.rasp_pi.set_servo_pulsewidth(self.PIN_YAW, int(self.yaw))
        self.rasp_pi.set_servo_pulsewidth(self.PIN_PITCH, int(self.pitch))
        self.rasp_pi.set_servo_pulsewidth(self.PIN_THROTTLE, int(self.throttle))

"""Construct plane"""
aero = plane()
aero.fly()
