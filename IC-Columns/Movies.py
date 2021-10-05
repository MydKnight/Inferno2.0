__author__ = 'shilohmadsen'
import os
# This file sends the UDP commands to localhost to trigger the play movie
import socket, subprocess, sentry_sdk

sentry_sdk.init(
    "https://11a17ec581624433b82658aafc16918e@o358570.ingest.sentry.io/5992300",
    traces_sample_rate=1.0,
)

blackhole = open(os.devnull, 'w')


def PlayMovie(file="intermission.mp4"):
    #print ("playing movie")

    UDP_IP = "localhost"
    UDP_PORT = 4444
    MESSAGE = "looper/play:%s" % (file)

    sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
    os.system('stty sane')
    #print "done playing movie"
    return

def StartLoop(LoopPath):
    new_env = os.environ.copy()
    new_env['INFOBEAMER_AUDIO_TARGET'] = 'hdmi'
    subprocess.Popen(['info-beamer-pi/info-beamer', LoopPath], env=new_env,  stdout=blackhole,
                     stderr=subprocess.STDOUT)
    #print "Starting Movie Loop"
    return

def StopLoop():
    subprocess.Popen(['sudo' ,'pkill', 'info-beamer'])
    #print "Starting Movie Loop"
    return

def PlayLoop ():
    UDP_IP = "localhost"
    UDP_PORT = 4444
    MESSAGE = "looper/loop:"

    sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
    os.system('stty sane')
    return