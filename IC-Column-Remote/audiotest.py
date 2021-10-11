import subprocess, random, glob, os

HellSortAudio = glob.glob(os.path.join('/HellSortAudio', '*.mp3'))

while True:
    player = subprocess.Popen(['mpg321', random.choice(HellSortAudio)], stdout=subprocess.DEVNULL)
    player.wait()