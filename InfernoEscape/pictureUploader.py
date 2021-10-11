import ftplib, os, glob

session = ftplib.FTP('shilohmadsen.com')
session.login(os.environ.get('ftpUser'),os.environ.get('ftpPass'))
session.cwd("//shilohmadsen.com//MagicCastle//InfernoPics//")
files = os.listdir("pictures")

def placeFiles():
    for file in files:
        print(file)
        session.storbinary('STOR ' + file, open('pictures/'+file,'rb'))
    session.quit()

placeFiles()
