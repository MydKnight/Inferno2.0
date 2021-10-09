# External module imports
import RPi.GPIO as GPIO
import sentry_sdk, Movies, time, os, serial, subprocess, WebService, random, glob, socket

sentry_sdk.init(
    "https://11a17ec581624433b82658aafc16918e@o358570.ingest.sentry.io/5992300",
    traces_sample_rate=1.0,
)

# Pin Definitons:
redLedPin = 16 
blueLedPin = 21 

# UDP Client
UDP_IP_ADDRESS = "192.168.40.163"
UDP_PORT_NO = 6789
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Pin Setup:
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
GPIO.setup(redLedPin, GPIO.OUT) 
GPIO.setup(blueLedPin, GPIO.OUT)

# Initial state for LEDs:
GPIO.output(redLedPin, GPIO.LOW)
GPIO.output(blueLedPin, GPIO.LOW)

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
        print(rfid)
        WebService.LogActivation(rfid, piid)
        # Play Pillar Video
        Movies.PlayMovie()
        time.sleep(10)
        Movies.PlayLoop()
        # Turn on Demon Eyes
        clientSock.sendto((os.environ.get('AssetFolder') + ",on").encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
        time.sleep(2)
        # Play Demon Sounds
        player = subprocess.Popen(['mpg321', '-q', random.choice(SatanAudio)])
        # Wait for sound file to end 
        player.wait()
        # Turn off Demon Eyes
        clientSock.sendto((os.environ.get('AssetFolder') + ",off").encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
        # Wait to Reset
        time.sleep(5)
        ser.reset_input_buffer()
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
