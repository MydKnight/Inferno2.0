# External module imports
import RPi.GPIO as GPIO
import sentry_sdk, Movies, time, os, serial, subprocess, WebService, random, glob

sentry_sdk.init(
    "https://11a17ec581624433b82658aafc16918e@o358570.ingest.sentry.io/5992300",
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

SatanAudio = glob.glob(os.path.join('/Audio', '*.mp3'))

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
        player = subprocess.Popen(['mpg321', random.choice(SatanAudio)])
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
