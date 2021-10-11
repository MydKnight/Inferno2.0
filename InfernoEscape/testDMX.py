import time
from DmxPy import DmxPy

dmx = DmxPy('serial port')

while True:
    dmx.setChannel(1, 255)
    time.sleep(3)
    dmx.setChannel(1, 0)
    time.sleep(3)