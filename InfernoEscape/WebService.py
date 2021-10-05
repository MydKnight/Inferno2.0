__author__ = 'shilohmadsen'
import requests, os, sentry_sdk
from requests.auth import HTTPBasicAuth

sentry_sdk.init(
    "https://3afa8408851043d78db36d6822534423@o358570.ingest.sentry.io/5992303",
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

def GetUser(rfid):
    response = requests.get('http://castlebackend-env.eba-5re8trqt.us-east-2.elasticbeanstalk.com/members/' + rfid, auth=HTTPBasicAuth(wsUsername, wsPassword))
    if response.status_code != 200:
        print("Member Retrieval Unsuccessful. Please view Backend Error")
    return response.text