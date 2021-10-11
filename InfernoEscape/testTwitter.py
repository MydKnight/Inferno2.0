import os
from twython import Twython
from dotenv import load_dotenv

load_dotenv()

# For uploading to Twitter
twitter = Twython(
    os.environ.get('twitter_key'),
    os.environ.get('twitter_secret'),
    os.environ.get('twitter_token'),
    os.environ.get('twitter_token_secret')
)

print (os.environ.get('twitter_token_secret'))

try:
    # photo = open(location, 'rb')
    # response = twitter.upload_media(media=photo)
    twitter.update_status(status="Test Message")
except Exception as e: 
    print (e)