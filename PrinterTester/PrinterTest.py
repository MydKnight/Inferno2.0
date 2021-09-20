# External module imports
import RPi.GPIO as GPIO
import sentry_sdk

sentry_sdk.init(
    "https://53058513222b41498b342be101261452@o358570.ingest.sentry.io/3153173",
    traces_sample_rate=1.0,
)

# Pin Definitons:
redLedPin = 16 
redButPin = 13 

# Pin Setup:
GPIO.setmode(GPIO.BCM) 
GPIO.setup(redLedPin, GPIO.OUT) 
GPIO.setup(redButPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# Initial state for LEDs:
GPIO.output(redLedPin, GPIO.LOW)

try:
    while 1:
        if GPIO.input(redButPin): # button is released
            GPIO.output(redLedPin, GPIO.LOW)
        else: # button is pressed:
            GPIO.output(redLedPin, GPIO.HIGH)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
