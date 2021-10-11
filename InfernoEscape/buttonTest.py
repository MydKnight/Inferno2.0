import RPi.GPIO as GPIO

redButPin = 13

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(redButPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

while True:
    if GPIO.input(redButPin): # button is released
        print ("Down")
    else:
        print ("Up")
    time.sleep(1)