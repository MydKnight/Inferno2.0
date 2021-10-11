import ftplib, os
from dotenv import load_dotenv

load_dotenv()

print("User: " + os.environ.get("ftpUser"))
session = ftplib.FTP('shilohmadsen.com',os.environ.get('ftpUser'),os.environ.get('ftpPass'))
file = open('boingo.mp3','rb')                  # file to send
session.cwd("//shilohmadsen.com//MagicCastle//InfernoPics//")
session.storbinary('STOR boingo.mp3', file)     # send the file
file.close()                                    # close file and FTP
session.quit()