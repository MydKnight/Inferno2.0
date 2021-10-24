import DMX, time

while True:
    dmxSetting = input("Please enter a Channel and Value:\n")
    dmxArray = dmxSetting.split()
    # print(dmxArray)
    DMX.setChannel(int(dmxArray[0]), int(dmxArray[1]))
    