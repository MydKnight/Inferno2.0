import serial, time

# Setup Serial Port
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600
)

while 1:
    rfid = ser.readline()
    print (rfid)