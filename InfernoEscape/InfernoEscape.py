# External module imports
import RPi.GPIO as GPIO
import sentry_sdk, picamera, time, os
from twython import Twython

sentry_sdk.init(
    "https://53058513222b41498b342be101261452@o358570.ingest.sentry.io/3153173",
    traces_sample_rate=1.0,
)

# For uploading to Twitter
twitter = Twython(
    os.environ.get('twitter_key'),
    os.environ.get('twitter_secret'),
    os.environ.get('twitter_token'),
    os.environ.get('twitter_token_secret')
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

def takePicture(location):
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            # Camera warm-up time
            time.sleep(1)
            picture = location + '/' + time.strftime("%Y%m%d-%H%M%S") + '.jpg'
            camera.capture(picture)
            # message = "Hello world!"
            # twitter.update_status(status=message)
            # print("Tweeted: %s" % message)
            # print ("Picture Taken")
    except Exception as e:
        print ("Unable to take picture: " + e)
        return

try:
    while 1:
        # Read if RFID was scanned within 10 seconds
        # Set Name of User and Level of Hell/ Generic from Hell
        # Log Activation
        # Determine Escape / Damnation
        # Activate Escape / Damnation Light
        # Play Sound
        # Take Picture
        # Upload Picture
        if GPIO.input(redButPin): # button is released
            GPIO.output(redLedPin, GPIO.LOW)
        else: # button is pressed:
            GPIO.output(redLedPin, GPIO.HIGH)
            takePicture("pictures")
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
