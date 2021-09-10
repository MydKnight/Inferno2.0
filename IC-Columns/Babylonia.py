# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
redLedPin = 16 # Broadcom pin 23 (P1 pin 16)
redButPin = 13 # Broadcom pin 17 (P1 pin 11)

# Pin Setup:
GPIO.setmode(GPIO.BCM) 
GPIO.setup(redLedPin, GPIO.OUT) # LED pin set as output
GPIO.setup(redButPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

# Initial state for LEDs:
GPIO.output(redLedPin, GPIO.LOW)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        if GPIO.input(redButPin): # button is released
            GPIO.output(redLedPin, GPIO.LOW)
        else: # button is pressed:
            GPIO.output(redLedPin, GPIO.HIGH)
            time.sleep(0.075)
            GPIO.output(redLedPin, GPIO.LOW)
            time.sleep(0.075)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
