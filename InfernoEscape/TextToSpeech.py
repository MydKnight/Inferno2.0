from gtts import gTTS
import os

def PlayText(message):
    language = 'en'
    try:
        myobj = gTTS(text=message, lang=language, slow=False)
        myobj.save("Inferno-Sort-Audio.mp3")
    
        # Play the converted file
        os.system("mpg321 Inferno-Sort-Audio.mp3") 
    except Exception as e:
        print ("Unable to Get Voice: " + str(e))