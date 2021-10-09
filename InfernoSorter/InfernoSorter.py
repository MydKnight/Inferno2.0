import random
import RPi.GPIO as GPIO
import sentry_sdk, os, threading, serial, Movies, glob, WebService, json, subprocess, time, socket
from datetime import datetime

sentry_sdk.init(
    "https://6b25279be7af4821a389db384ce3ded3@o358570.ingest.sentry.io/5992320",
    traces_sample_rate=1.0,
)

# Pin Definitons:
eightPin = 16 
twoPin = 21
fourPin = 20
onePin = 26
lightShowPin = 8
loadPin = 7
strobePin = 19
handSensorPin = 13

# Set up UDP Details
UDP_IP_ADDRESS = "192.168.40.242"
UDP_PORT_NO = 6789
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(onePin, GPIO.OUT) 
GPIO.setup(twoPin, GPIO.OUT)
GPIO.setup(fourPin, GPIO.OUT) 
GPIO.setup(eightPin, GPIO.OUT)  
GPIO.setup(loadPin, GPIO.OUT)  
GPIO.setup(lightShowPin, GPIO.OUT)  
GPIO.setup(strobePin, GPIO.OUT)  
GPIO.setup(handSensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# Initial state for LEDs:
GPIO.output(onePin, GPIO.LOW)
GPIO.output(twoPin, GPIO.LOW)
GPIO.output(fourPin, GPIO.LOW)
GPIO.output(eightPin, GPIO.LOW)
GPIO.output(loadPin, GPIO.LOW)
GPIO.output(strobePin, GPIO.LOW)
GPIO.output(lightShowPin, GPIO.LOW)

# Setup Serial Port
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600
)

HellSortAudio = glob.glob(os.path.join('/HellSortAudio', '*.mp3'))

GPIOMessagePins = {
    1: [onePin],
    2: [twoPin],
    3: [onePin, twoPin],
    4: [fourPin],
    5: [fourPin, onePin],
    6: [fourPin, twoPin],
    7: [fourPin, twoPin, onePin],
    8: [eightPin],
    9: [eightPin, onePin]
}

# PIID for Logging Activations
piid = os.environ.get('PIID')

# Start Movie Loop
Movies.StartLoop('Marquee')

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
    diff = lastScan - currentTime
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

def getMessage(rfid):
    message = "The Magic Castle Halloween 2021: Dante's Inferno"
    if rfid != '0':
        # Set Name of User and Level of Hell/ Generic from Hell
        user = getUserFromDatabase(rfid)
        if len(user['data']) > 0:
            FirstName = user['data'][0]['FirstName']
            LastName = user['data'][0]['LastName']
            HellLevel = parseHellLevel(user['data'][0]['HellLevel'], rfid)
            message = FirstName + " " + LastName + " is consigned to " + HellLevel + " !"
        else:
            HellLevel = parseHellLevel(None, rfid)
            message = "You are consigned to " + HellLevel + " !"    
    else:
        # No RFID. Randomly Assign a hell level
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
        HellLevel = mapping.get(random.randint(1,9), "The First Circle: Limbo")
        message = "You are consigned to " + HellLevel + " !"   
    
    return message

def getLevel(message):
    level = 1
    mapping = {
        "You are consigned to The First Circle: Limbo !": 1,
        "You are consigned to The Second Circle: Lust !": 2,
        "You are consigned to The Third Circle: Gluttony !": 3,
        "You are consigned to The Fourth Circle: Greed !": 4,
        "You are consigned to The Fifth Circle: Anger !": 5,
        "You are consigned to The Sixty Circle: Heresy !": 6,
        "You are consigned to The Seventh Circle: Violence !": 7,
        "You are consigned to The Eighth Circle: Fraud !": 8,
        "You are consigned to The Ninth Circle: Treachery !": 9
    }
    level = mapping.get(message, 1)
    return level

def lightHellLevel(level, state):
    pinArray = GPIOMessagePins.get(level)
    if state == "on":
        for pin in pinArray:
            GPIO.output(pin, GPIO.HIGH)
    else:
        for pin in pinArray:
            GPIO.output(pin, GPIO.LOW)

rfidLogger = threading.Thread(target=logRFIDRead, args=(1,))
rfidLogger.start()

while True:
    if GPIO.input(handSensorPin): # button is released
        GPIO.output(onePin, GPIO.LOW)
    else: # button is pressed:
        GPIO.output(onePin, GPIO.HIGH)
        # Read if RFID was scanned within 10 seconds
        rfid = confirmIdentity()
        
        WebService.LogActivation(rfid, piid)

        # Message to display on Marquee    
        message = getMessage(rfid)

        # Parse the user Hell Level and set DCBA
        level = getLevel(message)
        print ("Hell Level: " + str(level))
        lightHellLevel(level, "on")
        
        # Play Random Audio File and Lightshow
        player = subprocess.Popen(['mpg321', random.choice(HellSortAudio)], stdout=subprocess.DEVNULL)
        GPIO.output(lightShowPin, GPIO.HIGH)
        GPIO.output(loadPin, GPIO.HIGH)
        player.wait()
        
        # Stop Lightshow, Light Hell Level
        GPIO.output(loadPin, GPIO.LOW)

        # Play Movie for Hell Level and bell
        Movies.PlayMovie(str(level) + ".mp4")
        player = subprocess.Popen(['mpg321', random.choice(HellSortAudio)], stdout=subprocess.DEVNULL)
        time.sleep(6)

        # Strobe and Send UDP to Print Soul Reciept
        GPIO.output(strobePin, GPIO.HIGH)
        clientSock.sendto(str(level).encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
        time.sleep(6)

        # Reset (Movie, Pin State)
        Movies.PlayLoop()
        lightHellLevel(level, "off")
        GPIO.output(strobePin, GPIO.LOW)
        
        #Debugging only. This pin will not need to be set low. 
        GPIO.output(onePin, GPIO.LOW)
