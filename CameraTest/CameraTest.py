# External module imports
import RPi.GPIO as GPIO
import sentry_sdk, picamera, time, os
from instabot import Bot

sentry_sdk.init(
    "https://53058513222b41498b342be101261452@o358570.ingest.sentry.io/3153173",
    traces_sample_rate=1.0,
)

# For uploading to Instagram
instabot = Bot()
instabot.login(
    username = os.environ.get('IG_UserName'),
    password = os.environ.get('IG_Password')
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
            instabot.upload_photo(picture, caption ="Technical Scripter Event 2019")
            print ("Picture Taken")
    except (e):
        print ("Unable to take picture")
        capture_exception(e)
        return

try:
    while 1:
        if GPIO.input(redButPin): # button is released
            GPIO.output(redLedPin, GPIO.LOW)
        else: # button is pressed:
            GPIO.output(redLedPin, GPIO.HIGH)
            takePicture("pictures")
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
