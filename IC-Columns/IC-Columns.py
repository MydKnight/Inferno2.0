# External module imports
import RPi.GPIO as GPIO
import sentry_sdk, Movies, time, os, serial, subprocess, WebService

sentry_sdk.init(
    "https://53058513222b41498b342be101261452@o358570.ingest.sentry.io/3153173",
    traces_sample_rate=1.0,
)

# Pin Definitons:
redLedPin = 16 
blueLedPin = 21 

# Pin Setup:
GPIO.setmode(GPIO.BCM) 
GPIO.setup(redLedPin, GPIO.OUT) 
GPIO.setup(blueLedPin, GPIO.OUT)

# Initial state for LEDs:
GPIO.output(redLedPin, GPIO.LOW)
GPIO.output(blueLedPin, GPIO.LOW)

# Make Loud
subprocess.call(["amixer", "sset", "PCM", "100%"])

# Start Movie Loop
Movies.StartLoop(os.environ.get('AssetFolder'))

# Setup Serial Port
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600
)

# PIID for Logging Activations
piid = os.environ.get('PIID')

try:
    while 1:
        rfid = ser.readline()
        rfid = rfid.decode('utf-8').replace('\r\n', '')
        # Log Activation
        WebService.LogActivation(rfid, piid)
        # Turn on Pillar Spot
        GPIO.output(redLedPin, GPIO.HIGH)
        # Play Pillar Video
        Movies.PlayMovie()
        time.sleep(6)
        Movies.PlayLoop()
        # Turn off Pillar Spot and wait
        GPIO.output(redLedPin, GPIO.LOW)
        time.sleep(2)
        # Play Demon Sounds
        player = subprocess.Popen(['mpg321', os.environ.get('AssetFolder') + '/StoneSlide1.mp3'])
        # Turn on Demon Eyes
        GPIO.output(blueLedPin, GPIO.HIGH)
        # Wait for sound file to end 
        player.wait()
        # Turn off Demon Eyes
        GPIO.output(blueLedPin, GPIO.LOW)
        # Wait to Reset
        time.sleep(5)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
