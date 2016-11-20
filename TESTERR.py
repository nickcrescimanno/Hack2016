import pigpio
import time
pi = pigpio.pi()  # open local Pi

foundIt=False
for bus in xrange(100):
    for address in xrange(100):
        try:
            h = pi.i2c_open(bus, "0x"+str(address))
            time.sleep(10)
        except:
            print "not" + str(bus)
            bus+=1
