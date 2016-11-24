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
    # GPIO PIN OF PITCH SERVO
    PITCH_PIN = 10
    # GPIO PIN OF YAW SERVO
    YAW_PIN = 9
    # GPIO PIN OF THROTTLE SERVO
    THROTTLE_PIN = 11
    # raspberry pi pigpio object, API used to interface with Raspberry Pi
    rasp_pi = None
    # I2C Port
    I2C = 2
    # I2C Address
    I2C_ADDRESS = 0x68
    # BUS NUMBER
    BUS_NUM = 1
    # ACCEL
    ACCEL_ADDRESS = 0x3B

    """Connect to API, establishes connections to THROTTLE, PITCH, and YAW controls and
    initializes the I2C connection.
    """
    def __init__(self):
        self.rasp_pi = pigpio.pi()  # connect to local Pi
        self.rasp_pi.set_mode(self.THROTTLE_PIN, pigpio.OUTPUT)  # GPIO 17 as output
        self.rasp_pi.set_mode(self.PITCH_PIN, pigpio.OUTPUT)  # GPIO 17 as output
        self.rasp_pi.set_mode(self.YAW_PIN, pigpio.OUTPUT)  # GPIO 17 as output
        self.I2C = self.rasp_pi.i2c_open(self.BUS_NUM, self.I2C_ADDRESS)

    """Bit shifts two bits and scales the result to return the z accelation
    @param first
        first bit to shift
    @param second
        second bit to shift
    @return z_accel
        z axis acceleration of plane"""
    def get_z_accel(self, first, second):
        raw_accel = self.read_2_bits(first, second)
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
    def read_2_bits(self, first, second):
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
    def read_bytes(self, address, count, isAccelData):
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
                dec_values.append(self.read_2_bits(block_data[first], block_data[second]))
            first += 2
            second += 2
            index += 1
        return dec_values

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

    """Ensures {@code new_yaw} is valid. If {@code new_yaw} exceeds servo pwm bounds,
    {@code new_yaw} will be set to appropriate bound
    @return valid yaw"""
    def adjust_yaw(self, new_yaw):
        yaw = self.YAW_CENTER - new_yaw * self.RANGE
        if (self.MIN > yaw):
            yaw = self.MIN
        elif (self.MAX < yaw):
            yaw = self.MAX
        return yaw

    """Ensures {@code new_pitch} is valid. If {@code new_pitch} exceeds servo pwm bounds,
    {@code new_pitch} will be set to appropriate bound
    @return valid pitch"""
    def adjust_pitch(self,  new_pitch):
        pitch = self.PITCH_CENTER - new_pitch * self.RANGE
        if (self.MIN > pitch):
            pitch = self.MIN
        elif (self.MAX < pitch):
            pitch = self.MAX
        return pitch

    """Updates Yaw, Pitch and Throttle of plane according to {@code new_yaw},
       {@code new_pitch}, and {@code new_throttle}
    @updates self.rasp_pi"""
    def update_controls(self, new_yaw, new_pitch, new_throttle):
        """Update Yaw"""
        new_yaw = self.adjust_yaw(new_yaw)
        """Update Pitch"""
        new_pitch = self.adjust_pitch(new_pitch)
        """Update Throttle"""
        new_throttle = 1000 + new_throttle * self.THROTTLE_RANGE
        """Send new values to rasp_pi"""
        self.rasp_pi.set_servo_pulsewidth(self.YAW_PIN, int(new_yaw))
        self.rasp_pi.set_servo_pulsewidth(self.PITCH_PIN, int(new_pitch))
        self.rasp_pi.set_servo_pulsewidth(self.THROTTLE_PIN, int(new_throttle))

    """Flies the plane according to {@code ControllerInput}"""
    def fly(self):
        dOld=0
        controller = ControllerInput()
        while True:
            """Print Acceleration Data"""
            accel_data = self.read_bytes(self.ACCEL_ADDRESS, 6, True)
            (z, y, x) = (accel_data[0], accel_data[1], accel_data[2])
            print z,y,x
            """Monitor Controller Input"""
            new_yaw, new_pitch, new_throttle, d = controller.poll()
            """Trim if needed"""
            if d!=0 and dOld==0:
                for button in range(7):
                    if (d & 2**button) == 1:
                        self.trim(button)
            dOld = d
            """Update Controls"""
            self.update_controls(new_yaw, new_pitch, new_throttle)

"""Construct plane"""
aero = plane()
aero.fly()
