import RPi.GPIO as GPIO
import sentry_sdk, os, threading, serial, Movies

sentry_sdk.init(
    "https://53058513222b41498b342be101261452@o358570.ingest.sentry.io/3153173",
    traces_sample_rate=1.0,
)

# Pin Definitons:
redLedPin = 16 
blueLedPin = 21
redButPin = 13

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(redLedPin, GPIO.OUT) 
GPIO.setup(blueLedPin, GPIO.OUT) 
GPIO.setup(redButPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# Initial state for LEDs:
GPIO.output(redLedPin, GPIO.LOW)
GPIO.output(blueLedPin, GPIO.LOW)

# Setup Serial Port
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600
)

# Start Movie Loop
Movies.StartLoop('Marquee'))

while True:
    time.sleep(2)
    Movies.PlayMovie("foo")
