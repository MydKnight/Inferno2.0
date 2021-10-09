# External module imports
import RPi.GPIO as GPIO
import sentry_sdk, time, random

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

try:
    while 1:
        flicker = random.choice([redLedPin, blueLedPin, greenLedPin])
        print (str(flicker))
        GPIO.output(flicker, GPIO.HIGH)
        time.sleep(10)
        GPIO.output(flicker, GPIO.LOW)
        time.sleep(60)
        print("Cycle Complete")

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
