class calc():
    def __init__(self):
        print ""

    """Gets Value from two indexes of bit array
        @param first
            bit[0]
        @param second
            bit[1]
    """
    def calc(self, first, second):
        val = (first << 8) + second
        if val >= 2 ** 15:
            val = val - 2 ** 16 - 1  # bit shi
        val = val / 16384.0
        return val

    def writeByte(self, address, hval):
        pi.i2c_write_byte_data(h, address, hval)  # wake up mpu6050

    def readBytes(self, address, count):
        bites = []
        val = []
        z = pi.i2c_read_i2c_block_data(h, address, count)
        count = 0
        for i in z:
            bites.extend(i)
            count += 1
        for i in range(0, count, 2):
            a = calc()
            val = a.calc(bites[i], bites[i + 1])
            bites[i]
        return val