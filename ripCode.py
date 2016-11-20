from calc import calc
import pigpio
import time

gyroBias=[]
accelBias=[]
XGOFFS_TC = 0x00  # Bit 7 PWR_MODE, bits 6:1 XG_OFFS_TC, bit 0 OTP_BNK_VLD
YGOFFS_TC = 0x01
ZGOFFS_TC = 0x02
X_FINE_GAIN = 0x03  # [7:0] fine gain
Y_FINE_GAIN = 0x04
Z_FINE_GAIN = 0x05
XA_OFFSET_H = 0x06  # User-defined trim values for accelerometer
XA_OFFSET_L_TC = 0x07
YA_OFFSET_H = 0x08
YA_OFFSET_L_TC = 0x09
ZA_OFFSET_H = 0x0A
ZA_OFFSET_L_TC = 0x0B
SELF_TEST_X = 0x0D
SELF_TEST_Y = 0x0E
SELF_TEST_Z = 0x0F
SELF_TEST_A = 0x10
XG_OFFS_USRH = 0x13  # User-defined trim values for gyroscope supported in MPU-6050?
XG_OFFS_USRL = 0x14
YG_OFFS_USRH = 0x15
YG_OFFS_USRL = 0x16
ZG_OFFS_USRH = 0x17
ZG_OFFS_USRL = 0x18
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
FF_THR = 0x1D  # Free-fall
FF_DUR = 0x1E  # Free-fall
MOT_THR = 0x1F  # Motion detection threshold bits [7:0]
MOT_DUR = 0x20  # Duration counter threshold for motion interrupt generation, 1 kHz rate, LSB = 1 ms
ZMOT_THR = 0x21  # Zero-motion detection threshold bits [7:0]
ZRMOT_DUR = 0x22  # Duration counter threshold for zero motion interrupt generation, 16 Hz rate, LSB = 64 ms
FIFO_EN = 0x23
I2C_MST_CTRL = 0x24
I2C_SLV0_ADDR = 0x25
I2C_SLV0_REG = 0x26
I2C_SLV0_CTRL = 0x27
I2C_SLV1_ADDR = 0x28
I2C_SLV1_REG = 0x29
I2C_SLV1_CTRL = 0x2A
I2C_SLV2_ADDR = 0x2B
I2C_SLV2_REG = 0x2C
I2C_SLV2_CTRL = 0x2D
I2C_SLV3_ADDR = 0x2E
I2C_SLV3_REG = 0x2F
I2C_SLV3_CTRL = 0x30
I2C_SLV4_ADDR = 0x31
I2C_SLV4_REG = 0x32
I2C_SLV4_DO = 0x33
I2C_SLV4_CTRL = 0x34
I2C_SLV4_DI = 0x35
I2C_MST_STATUS = 0x36
INT_PIN_CFG = 0x37
INT_ENABLE = 0x38
DMP_INT_STATUS = 0x39  # Check DMP interrupt
INT_STATUS = 0x3A
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48
EXT_SENS_DATA_00 = 0x49
EXT_SENS_DATA_01 = 0x4A
EXT_SENS_DATA_02 = 0x4B
EXT_SENS_DATA_03 = 0x4C
EXT_SENS_DATA_04 = 0x4D
EXT_SENS_DATA_05 = 0x4E
EXT_SENS_DATA_06 = 0x4F
EXT_SENS_DATA_07 = 0x50
EXT_SENS_DATA_08 = 0x51
EXT_SENS_DATA_09 = 0x52
EXT_SENS_DATA_10 = 0x53
EXT_SENS_DATA_11 = 0x54
EXT_SENS_DATA_12 = 0x55
EXT_SENS_DATA_13 = 0x56
EXT_SENS_DATA_14 = 0x57
EXT_SENS_DATA_15 = 0x58
EXT_SENS_DATA_16 = 0x59
EXT_SENS_DATA_17 = 0x5A
EXT_SENS_DATA_18 = 0x5B
EXT_SENS_DATA_19 = 0x5C
EXT_SENS_DATA_20 = 0x5D
EXT_SENS_DATA_21 = 0x5E
EXT_SENS_DATA_22 = 0x5F
EXT_SENS_DATA_23 = 0x60
MOT_DETECT_STATUS = 0x61
I2C_SLV0_DO = 0x63
I2C_SLV1_DO = 0x64
I2C_SLV2_DO = 0x65
I2C_SLV3_DO = 0x66
I2C_MST_DELAY_CTRL = 0x67
SIGNAL_PATH_RESET = 0x68
MOT_DETECT_CTRL = 0x69
USER_CTRL = 0x6A  # Bit 7 enable DMP, bit 3 reset DMP
PWR_MGMT_1 = 0x6B  # Device defaults to the SLEEP mode
PWR_MGMT_2 = 0x6C
DMP_BANK = 0x6D  # Activates a specific bank in the DMP
DMP_RW_PNT = 0x6E  # Set read/write pointer to a specific start address in specified DMP bank
DMP_REG = 0x6F  # Register in DMP from which to read or to which to write
DMP_REG_1 = 0x70
DMP_REG_2 = 0x71
FIFO_COUNTH = 0x72
FIFO_COUNTL = 0x73
FIFO_R_W = 0x74
WHO_AM_I_MPU6050 = 0x75  # Should return = 0x68
pi = pigpio.pi()  # open local Pi

h = pi.i2c_open(1, 0x68)


"""Gets Value from two indexes of bit array
@param first
    bit[0]
@param second
    bit[1]
"""
def getVal(first, second):
    val = readVal(first, second)
    val = val / 16384.0
    return val

def readVal(first, second):
    val = (first << 8) | second
    if val >= 2 ** 15:
        val = val - 2 ** 16 - 1  # bit shi
    return val

def writeByte(address, hval):
    pi.i2c_write_byte_data(h, address, hval)  # wake up mpu6050

def readBytes(address, count, isData):
    bites = []
    (s,z) = pi.i2c_read_i2c_block_data(h, address, count)
    index = 0
    first = 0
    second = 1
    while second < count:
        if isData:
            bites.append(getVal(z[first], z[second]))
        else:
            bites.append(readVal(z[first], z[second]))
        first+=2
        second+=2
        index+=1
    return bites


def readByte(y):
    b = pi.i2c_read_byte_data(h, y)
    return b


def calibrateMPU6050(dest1, dest2):
    gyro_bias = [0, 0, 0]
    accel_bias = [0, 0, 0]

    # reset device, reset all registers, clear gyro and accelerometer bias registers
    writeByte(PWR_MGMT_1, 0x80)  # Write a one to bit 7 reset bit toggle reset device
    time.sleep(.1)

    # get stable time source
    # Set clock source to be PLL with x-axis gyroscope reference, bits 2:0 = 001
    writeByte(PWR_MGMT_1, 0x01)
    writeByte(PWR_MGMT_2, 0x00)
    time.sleep(.2)

    # Configure device for bias calculation
    writeByte(INT_ENABLE, 0x00)  # Disable all interrupts
    writeByte(FIFO_EN, 0x00)  # Disable FIFO
    writeByte(PWR_MGMT_1, 0x00)  # Turn on internal clock source
    writeByte(I2C_MST_CTRL, 0x00)  # Disable I2C master
    writeByte(USER_CTRL, 0x00)  # Disable FIFO and I2C master modes
    writeByte(USER_CTRL, 0x0C)  # Reset FIFO and DMP
    time.sleep(.015)

    # Configure MPU6050 gyro and accelerometer for bias calculation
    writeByte(CONFIG, 0x01)  # Set low-pass filter to 188 Hz
    writeByte(SMPLRT_DIV, 0x00)  # Set sample rate to 1 kHz
    writeByte(GYRO_CONFIG, 0x00)  # Set gyro full-scale to 250 degrees per second, maximum sensitivity
    writeByte(ACCEL_CONFIG, 0x00)  # Set accelerometer full-scale to 2 g, maximum sensitivity

    gyrosensitivity = 131  # = 131 LSB/degrees/sec
    accelsensitivity = 16384  # = 16384 LSB/g

    # Configure FIFO to capture accelerometer and gyro data for bias calculation
    writeByte(USER_CTRL, 0x40)  # Enable FIFO
    writeByte(FIFO_EN, 0x78)  # Enable gyro and accelerometer sensors for FIFO  (max size 1024 bytes in MPU-6050)
    time.sleep(.08)  # accumulate 80 samples in 80 milliseconds = 960 bytes

    # At end of sample accumulation, turn off FIFO sensor read
    writeByte(FIFO_EN, 0x00)  # Disable gyro and accelerometer sensors for FIFO
    fifo_count = readBytes(FIFO_COUNTH, 2)[0] # read FIFO sample count
    packet_count = fifo_count / 12  # How many sets of full gyro and accelerometer data for averaging
    print packet_count
    print fifo_count

    for i in xrange(packet_count):
        accel_temp = [0, 0, 0]
        gyro_temp = [0, 0, 0]
        data = readBytes(FIFO_R_W, 12)  # read data for averaging
        for x in xrange(3):
            accel_temp[x] = data[x]
        for x in xrange(3, 5, 3):
            gyro_temp[x] = data[x]

        accel_bias[0] += accel_temp[0]  # Sum individual signed 16-bit biases to get accumulated signed 32-bit biases
        accel_bias[1] += accel_temp[1]
        accel_bias[2] += accel_temp[2]
        gyro_bias[0] += gyro_temp[0]
        gyro_bias[1] += gyro_temp[1]
        gyro_bias[2] += gyro_temp[2]

    accel_bias[0] /= packet_count  # Normalize sums to get average count biases
    accel_bias[1] /= packet_count
    accel_bias[2] /= packet_count
    gyro_bias[0] /= (packet_count)
    gyro_bias[1] /= packet_count
    gyro_bias[2] /= packet_count

    if (accel_bias[2] > 0L):
        accel_bias[2] -= accelsensitivity  # Remove gravity from the z-axis accelerometer bias calculation
    else:
        accel_bias[2] += accelsensitivity

    # Construct the gyro biases for push to the hardware gyro bias registers, which are reset to zero upon device startup
    data[0] = (-gyro_bias[
        0] / 4 >> 8) & 0xFF  # Divide by 4 to get 32.9 LSB per deg/s to conform to expected bias input format
    data[1] = (-gyro_bias[0] / 4) & 0xFF  # Biases are additive, so change sign on calculated average gyro biases
    data[2] = (-gyro_bias[1] / 4 >> 8) & 0xFF
    data[3] = (-gyro_bias[1] / 4) & 0xFF
    data[4] = (-gyro_bias[2] / 4 >> 8) & 0xFF
    data[5] = (-gyro_bias[2] / 4) & 0xFF

    # Push gyro biases to hardware registers works well for gyro but not for accelerometer
    #  writeByte(MPU6050_ADDRESS, XG_OFFS_USRH, data[0])
    #  writeByte(MPU6050_ADDRESS, XG_OFFS_USRL, data[1])
    #  writeByte(MPU6050_ADDRESS, YG_OFFS_USRH, data[2])
    #  writeByte(MPU6050_ADDRESS, YG_OFFS_USRL, data[3])
    #  writeByte(MPU6050_ADDRESS, ZG_OFFS_USRH, data[4])
    #  writeByte(MPU6050_ADDRESS, ZG_OFFS_USRL, data[5])

    dest1[0] = 1.0 * gyro_bias[0] / 1.0 * gyrosensitivity  # construct gyro bias in deg/s for later manual subtraction
    dest1[1] = 1.0 * gyro_bias[1] / 1.0 * gyrosensitivity
    dest1[2] = 1.0 * gyro_bias[2] / 1.0 * gyrosensitivity

    # Construct the accelerometer biases for push to the hardware accelerometer bias registers. These registers contain
    # factory trim values which must be added to the calculated accelerometer biases on boot up these registers will hold
    # non-zero values. In addition, bit 0 of the lower byte must be preserved since it is used for temperature
    # compensation calculations. Accelerometer bias registers expect bias input as 2048 LSB per g, so that
    # the accelerometer biases calculated above must be divided by 8.

    accel_bias_reg = [0, 0, 0]  # A place to hold the factory accelerometer trim biases
    data = readBytes(XA_OFFSET_H, 2)  # Read factory accelerometer trim values
    accel_bias_reg[0] = data[0]
    data = readBytes(YA_OFFSET_H, 2)  # Read factory accelerometer trim values
    accel_bias_reg[1] = data[0]
    data = readBytes(ZA_OFFSET_H, 2)  # Read factory accelerometer trim values
    accel_bias_reg[2] = data[0]

    mask_bit = [0, 0, 0]  # Define array to hold mask bit for each accelerometer bias axis

    for i in xrange(3):
        if (accel_bias_reg[i] & 1):
            mask_bit[i] = 0x01  # If temperature compensation bit is set, record that fact in mask_bit

    # Construct total accelerometer bias, including calculated average accelerometer bias from above
    accel_bias_reg[0] -= (
        accel_bias[0] / 8)  # Subtract calculated averaged accelerometer bias scaled to 2048 LSB/g (16 g full scale)
    accel_bias_reg[1] -= (accel_bias[1] / 8)
    accel_bias_reg[2] -= (accel_bias[2] / 8)

    data[0] = (accel_bias_reg[0] >> 8) & 0xFF
    data[1] = (accel_bias_reg[0]) & 0xFF
    data[1] = data[1] | mask_bit[
        0]  # preserve temperature compensation bit when writing back to accelerometer bias registers
    data[2] = (accel_bias_reg[1] >> 8) & 0xFF
    data[3] = (accel_bias_reg[1]) & 0xFF
    data[3] = data[3] | mask_bit[
        1]  # preserve temperature compensation bit when writing back to accelerometer bias registers
    data[4] = (accel_bias_reg[2] >> 8) & 0xFF
    data[5] = (accel_bias_reg[2]) & 0xFF
    data[5] = data[5] | mask_bit[
        2]  # preserve temperature compensation bit when writing back to accelerometer bias registers

    # Push accelerometer biases to hardware registers doesn't work well for accelerometer
    # Are we handling the temperature compensation bit correctly?
    #  writeByte(MPU6050_ADDRESS, XA_OFFSET_H, data[0])
    #  writeByte(MPU6050_ADDRESS, XA_OFFSET_L_TC, data[1])
    #  writeByte(MPU6050_ADDRESS, YA_OFFSET_H, data[2])
    #  writeByte(MPU6050_ADDRESS, YA_OFFSET_L_TC, data[3])
    #  writeByte(MPU6050_ADDRESS, ZA_OFFSET_H, data[4])
    #  writeByte(MPU6050_ADDRESS, ZA_OFFSET_L_TC, data[5])

    # Output scaled accelerometer biases for manual subtraction in the main program
    dest2[0] = 1.0 * accel_bias[0] / 1.0 * accelsensitivity
    dest2[1] = 1.0 * accel_bias[1] / 1.0 * accelsensitivity
    dest2[2] = 1.0 * accel_bias[2] / 1.0 * accelsensitivity

    # Accelerometer and gyroscope self test check calibration wrt factory settings

    def MPU6050SelfTest(
            destination):  # Should return percent deviation from factory trim values, +/- 14 or less deviation is a pass

        rawData = [0,0,0,0]
        # Configure the accelerometer for self-test
        writeByte(ACCEL_CONFIG, 0xF0)  # Enable self test on all three axes and set accelerometer range to +/- 8 g
        writeByte(GYRO_CONFIG, 0xE0)  # Enable self test on all three axes and set gyro range to +/- 250 degrees/s
        time.sleep(.250)  # Delay a while to let the device execute the self-test
        rawData[0] = readByte(SELF_TEST_X)  # X-axis self-test results
        rawData[1] = readByte(SELF_TEST_Y)  # Y-axis self-test results
        rawData[2] = readByte(SELF_TEST_Z)  # Z-axis self-test results
        rawData[3] = readByte(SELF_TEST_A)  # Mixed-axis self-test results
        # Extract the acceleration test results first

        selfTest = [0, 0, 0, 0, 0, 0]
        selfTest[0] = (rawData[0] >> 3) | (rawData[3] & 0x30) >> 4  # XA_TEST result is a five-bit unsigned integer
        selfTest[1] = (rawData[1] >> 3) | (rawData[3] & 0x0C) >> 4  # YA_TEST result is a five-bit unsigned integer
        selfTest[2] = (rawData[2] >> 3) | (rawData[3] & 0x03) >> 4  # ZA_TEST result is a five-bit unsigned integer
        # Extract the gyration test results first
        selfTest[3] = rawData[0] & 0x1F  # XG_TEST result is a five-bit unsigned integer
        selfTest[4] = rawData[1] & 0x1F  # YG_TEST result is a five-bit unsigned integer
        selfTest[5] = rawData[2] & 0x1F  # ZG_TEST result is a five-bit unsigned integer
        # Process results to allow final comparison with factory set values
        factoryTrim = [0, 0, 0, 0, 0]
        factoryTrim[0] = (4096.0 * 0.34) * (
            pow((0.92 / 0.34), ((1.0 * selfTest[0] - 1.0) / 30.0)))  # FT[Xa] factory trim calculation
        factoryTrim[1] = (4096.0 * 0.34) * (
            pow((0.92 / 0.34), ((1.0 * selfTest[1] - 1.0) / 30.0)))  # FT[Ya] factory trim calculation
        factoryTrim[2] = (4096.0 * 0.34) * (
            pow((0.92 / 0.34), ((1.0 * selfTest[2] - 1.0) / 30.0)))  # FT[Za] factory trim calculation
        factoryTrim[3] = (25.0 * 131.0) * (pow(1.046, (1.0 * selfTest[3] - 1.0)))  # FT[Xg] factory trim calculation
        factoryTrim[4] = (-25.0 * 131.0) * (pow(1.046, (1.0 * selfTest[4] - 1.0)))  # FT[Yg] factory trim calculation
        factoryTrim[5] = (25.0 * 131.0) * (pow(1.046, (1.0 * selfTest[5] - 1.0)))  # FT[Zg] factory trim calculation

        #  Output self-test results and factory trim calculation if desired
        #  Serial.println(selfTest[0]) Serial.println(selfTest[1]) Serial.println(selfTest[2])
        #  Serial.println(selfTest[3]) Serial.println(selfTest[4]) Serial.println(selfTest[5])
        #  Serial.println(factoryTrim[0]) Serial.println(factoryTrim[1]) Serial.println(factoryTrim[2])
        #  Serial.println(factoryTrim[3]) Serial.println(factoryTrim[4]) Serial.println(factoryTrim[5])

        # Report results as a ratio of (STR - FT)/FT the change from Factory Trim of the Self-Test Response
        # To get to percent, must multiply by 100 and subtract result from 100
        destination = []
        for i in xrange(6):
            destination.append(100.0 + 100.0 * 1.0 * (selfTest[i] - factoryTrim[i]) / factoryTrim[i])  # Report percent differences



aRes = 2.0/326768.0
calibrateMPU6050(gyroBias, accelBias)
while True:
    vals = readBytes(0x3B, 6)
    for i in range(len(vals)):
        print vals[i]*aRes-accelBias[i]

