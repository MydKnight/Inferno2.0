import time

timer = time.time()

while True:
    current = time.time()
    if current - timer > 10:
        timer = current
        print ("Fire!")
    else:
        pass