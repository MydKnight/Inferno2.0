from dmxpy import DmxPy

# Todo: Create an interface here where we can select the DMX product and channel mode so that a single instantiation 
# Gets you a common interface

dmx = DmxPy.DmxPy('/dev/ttyUSB0')
dmx.blackout()
# Using 6 Channel, so we need to set the Master dimmer (6) to 255
dmx.set_channel(6,255)

def setChannel(channel, level):
    print("Setting channel: " + str(channel))
    print (type(channel))
    print ("Setting Level: " + str(level))
    print (type(level))
    dmx.set_channel(channel, level)
    dmx.render()