import pyttsx3

def PlayText(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 125) 
    engine.say(message)
    engine.runAndWait()