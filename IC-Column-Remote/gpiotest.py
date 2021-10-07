import time
import RPi.GPIO as GPIO

# Pin Definitons:
redLedPin = 16 
blueLedPin = 21 
greenLedPin = 20

# Pin Setup:
GPIO.setmode(GPIO.BCM) 
GPIO.setup(redLedPin, GPIO.OUT) 
GPIO.setup(blueLedPin, GPIO.OUT)
GPIO.setup(greenLedPin, GPIO.OUT)

# Initial state for LEDs:
GPIO.output(redLedPin, GPIO.LOW)
GPIO.output(blueLedPin, GPIO.LOW)
GPIO.output(greenLedPin, GPIO.LOW)

while True:
    GPIO.output(redLedPin, GPIO.HIGH)
    GPIO.output(blueLedPin, GPIO.HIGH)
    GPIO.output(greenLedPin, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(redLedPin, GPIO.LOW)
    GPIO.output(blueLedPin, GPIO.LOW)
    GPIO.output(greenLedPin, GPIO.LOW)
    time.sleep(3)