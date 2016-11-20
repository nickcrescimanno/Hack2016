import pigpio
pi = pigpio.pi()  # open local Pi

foundIt=False
for bus in xrange(100):
    for address in xrange(100):
        try:
            h = pi.i2c_open(bus, "0x"+str(address))
            break
        except:
            print "not" + str(bus)
            bus+=1
