__author__ = 'shilohmadsen'
import requests, os, sentry_sdk
from requests.auth import HTTPBasicAuth

sentry_sdk.init(
    "https://11a17ec581624433b82658aafc16918e@o358570.ingest.sentry.io/5992300",
    traces_sample_rate=1.0,
)

wsUsername = os.environ.get('WS_Username')
wsPassword = os.environ.get('WS_Password')

def LogActivation(rfid, piid):
    response = requests.post('http://castlebackend-env.eba-5re8trqt.us-east-2.elasticbeanstalk.com/activation/', data = {
        "RFID": rfid,
        "PIID": piid,
        "ActivationType": 2
    }, auth=HTTPBasicAuth(wsUsername, wsPassword))
    if response.status_code != 200:
        print("Activation Write Unsuccessful. Please view Backend Error")
    return