# External module imports
from sys import builtin_module_names
import RPi.GPIO as GPIO
import sentry_sdk, picamera, time, os, threading, serial, WebService, json, random, subprocess, glob
from datetime import datetime
from twython import Twython
from sentry_sdk import capture_exception

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

SalvationLines = glob.glob(os.path.join('/SalvationAudio', '*.mp3'))
DamnationLines = glob.glob(os.path.join('/DamnationAudio', '*.mp3'))

# PIID for Logging Activations
piid = os.environ.get('PIID')

def takePicture(location):
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            # Camera warm-up time
            time.sleep(1)
            picture = location + '/' + time.strftime("%Y%m%d-%H%M%S") + '.jpg'
            camera.capture(picture)
            return picture
    except Exception as e:
        print ("Unable to take picture: " + e)
        capture_exception(e)
        return

def postPicture(location, message="Lost Soul has Escaped!"):
    try:
        photo = open(location, 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=message, media_ids=[response['media_id']])
    except Exception as e: 
        print (e)
        capture_exception(e)

# Thread function to capture RFID reads in parallel
def logRFIDRead(name):
    try:
        while 1:
            rfid = ser.readline()
            rfid = rfid.decode('utf-8').replace('\r\n', '')
            loggedTime = datetime.now()
            f = open("rfidActivations.txt", "w")
            f.write(loggedTime.strftime("%m/%d/%Y %H:%M:%S") + "," + rfid)
            f.close()
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print ("exiting")

def confirmIdentity():
    currentTime = datetime.now()
    rfid = '0'

    # Get Last Read LIne
    with open("rfidActivations.txt") as f:
        firstLine = f.readline().rstrip()

    # Compare Last time to current
    string_list = firstLine.split(",")
    lastScan = datetime.strptime(string_list[0], "%m/%d/%Y %H:%M:%S")
    diff = currentTime - lastScan
    wholeSeconds = int(diff.total_seconds())
    
    # If Less than 10 seconds, write RFID variable
    if wholeSeconds < 300:
        rfid = string_list[1]

    return rfid

def getUserFromDatabase(rfid):
    userData = {}
    userData = WebService.GetUser(rfid)
    
    return json.loads(userData)

def parseHellLevel(hellLevel, rfid):
    parsedHellLevel = "The First Circle: Limbo"
    
    if hellLevel == None:
        # Designate based on RFID
        if rfid[0] == "1" or  rfid[0] == "2":
            hellLevel == 1
        if rfid[0] == "3" or  rfid[0] == "4":
            hellLevel == 2
        if rfid[0] == "5" or  rfid[0] == "6":
            hellLevel == 3
        if rfid[0] == "7" or  rfid[0] == "8":
            hellLevel == 4
        if rfid[0] == "9" or  rfid[0] == "A":
            hellLevel == 5
        if rfid[0] == "B" or  rfid[0] == "C":
            hellLevel == 6
        if rfid[0] == "D":
            hellLevel == 7
        if rfid[0] == "E":
            hellLevel == 8
        if rfid[0] == "F":
            hellLevel == 9

    # Once we have a level, translate that to text
    mapping = {
        1: "The First Circle: Limbo",
        2: "The Second Circle: Lust",
        3: "The Third Circle: Gluttony",
        4: "The Fourth Circle: Greed",
        5: "The Fifth Circle: Anger",
        6: "The Sixth Circle: Heresy",
        7: "The Seventh Circle: Violence",
        8: "The Eighth Circle: Fraud",
        9: "The Ninth Circle: Treachery"
    }
    parsedHellLevel = mapping.get(hellLevel, "The First Circle: Limbo")

    return parsedHellLevel

def getMessage(determination, rfid):
    message = "The Magic Castle Halloween 2021: Dante's Inferno"
    if rfid != '0':
        print ("We have an RFID Number")
        # Set Name of User and Level of Hell/ Generic from Hell
        user = getUserFromDatabase(rfid)
        if len(user['data']) > 0:
            FirstName = user['data'][0]['FirstName']
            LastName = user['data'][0]['LastName']
            HellLevel = parseHellLevel(user['data'][0]['HellLevel'], rfid)
        
            if determination == 0:
                message = FirstName + " " + LastName + " has escaped " + HellLevel + "!"
            else:
                message = FirstName + " " + LastName + " was damned to " + HellLevel + " for all eternity!"
        else:
            if determination == 0:
                message = "A Lost Soul has escaped Hell!"
            else:
                message = "A Lost Soul was damned for all eternity!"    
    else:
        if determination == 0:
            message = "A Lost Soul has escaped Hell!"
        else:
            message = "A Lost Soul was damned for all eternity!"
    
    return message

rfidLogger = threading.Thread(target=logRFIDRead, args=(1,))
rfidLogger.start()

try:
    while 1:
        if GPIO.input(redButPin): # button is released
            GPIO.output(redLedPin, GPIO.LOW)
        else: # button is pressed:
            # Read if RFID was scanned within 10 seconds
            rfid = confirmIdentity()
            
            WebService.LogActivation(rfid, piid)
            
            # Determine Escape (0) / Damnation (1)
            soulDetermination = random.choice([0, 1])

            # Activate Escape / Damnation Sequence
            if soulDetermination == 0:
                GPIO.output(redLedPin, GPIO.HIGH)
                player = subprocess.Popen(['mpg321', random.choice(SalvationLines)])
            else:
                GPIO.output(blueLedPin, GPIO.HIGH)
                player = subprocess.Popen(['mpg321', random.choice(DamnationLines)])
            
            message = getMessage(soulDetermination, rfid)
            player.wait()

            # Take Picture
            picture = takePicture("pictures")
            
            # Upload Picture
            postPicture(picture, message)

            # Lights Out
            GPIO.output(blueLedPin, GPIO.LOW)
            GPIO.output(redLedPin, GPIO.LOW)

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
