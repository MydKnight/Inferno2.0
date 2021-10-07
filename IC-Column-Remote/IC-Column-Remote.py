# External module imports
import RPi.GPIO as GPIO
import sentry_sdk, socket

sentry_sdk.init(
    "https://11a17ec581624433b82658aafc16918e@o358570.ingest.sentry.io/5992300",
    traces_sample_rate=1.0,
)

# Pin Definitons:
redLedPin = 16 
blueLedPin = 21 
greenLedPin = 20

# Simple UDP Server
UDP_IP_ADDRESS = "192.168.40.163"
UDP_PORT_NO = 6789
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

# Pin Setup:
GPIO.setmode(GPIO.BCM) 
GPIO.setup(redLedPin, GPIO.OUT) 
GPIO.setup(blueLedPin, GPIO.OUT)
GPIO.setup(greenLedPin, GPIO.OUT)

# Initial state for LEDs:
GPIO.output(redLedPin, GPIO.LOW)
GPIO.output(blueLedPin, GPIO.LOW)
GPIO.output(greenLedPin, GPIO.LOW)

try:
    while 1:
        data, addr = serverSock.recvfrom(1024)
        data = data.decode('utf-8')
        print ("Message: ", data)
        # Split Column from State
        splitData = data.split(",")
        if (splitData[0] == "LeftColumn"):
            if (splitData[1] == "on"):
                GPIO.output(redLedPin, GPIO.HIGH)
            else:
                GPIO.output(redLedPin, GPIO.LOW)
        elif (splitData[0] == "MiddleColumn"):
            if (splitData[1] == "on"):
                GPIO.output(blueLedPin, GPIO.HIGH)
            else:
                GPIO.output(blueLedPin, GPIO.LOW)
        else:
            if (splitData[1] == "on"):
                GPIO.output(greenLedPin, GPIO.HIGH)
            else:
                GPIO.output(greenLedPin, GPIO.LOW)
        
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
