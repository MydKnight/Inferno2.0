import time

# Pin Definitons:
eightPin = 16 
twoPin = 21
fourPin = 20
onePin = 26
lightShowPin = 8
loadPin = 7
strobePin = 19
handSensorPin = 13

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(onePin, GPIO.OUT) 
GPIO.setup(twoPin, GPIO.OUT)
GPIO.setup(fourPin, GPIO.OUT) 
GPIO.setup(eightPin, GPIO.OUT)  
GPIO.setup(loadPin, GPIO.OUT)  

# Initial state for LEDs:
GPIO.output(onePin, GPIO.LOW)
GPIO.output(twoPin, GPIO.LOW)
GPIO.output(fourPin, GPIO.LOW)
GPIO.output(eightPin, GPIO.LOW)
GPIO.output(loadPin, GPIO.LOW)

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

def lightHellLevel(level, state):
    pinArray = GPIOMessagePins.get(int(level))
    if state == "on":
        for pin in pinArray:
            GPIO.output(pin, GPIO.HIGH)
    else:
        for pin in pinArray:
            GPIO.output(pin, GPIO.LOW)

while True:
    level = input("Level?")
    lightHellLevel(level, "on")
    GPIO.output(loadPin, GPIO.LOW)
    GPIO.output(lightShowPin, GPIO.LOW)
    time.sleep(3)
    lightHellLevel(level, "off")