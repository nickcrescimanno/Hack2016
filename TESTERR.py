import pigpio
pi = pigpio.pi()  # open local Pi

foundIt=False
bus=0
while not foundIt:
    try:
        h = pi.i2c_open(bus, 0x68)
        foundIt = True
    except:
        bus+=1