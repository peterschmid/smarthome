#!/usr/bin/python

import sys, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


if len(sys.argv) != 2:
    print "Use first Argument as picture file name"
    sys.exit(0)
filenamePic = str(sys.argv[1])

#print filenameData
def readFromMailAdrAndPwAndToMailAdr():
  f=open("mail.txt", "r")
  content = f.readlines()
  content = [x.strip('\n') for x in content]
  return content[0], content[1], content[2]

def sendMail(sub, text, filename):
  # Prepare sending Mail and credentians
  fromaddr, password, toaddr =  readFromMailAdrAndPwAndToMailAdr()
  username = fromaddr

  # Create the root message and fill in the from, to, and subject headers
  msg = MIMEMultipart()
  msg['Subject'] = sub
  msg['From'] = fromaddr
  msg['To'] = toaddr
  
  msg.attach(MIMEText(text))
  fp = open(filename, 'rb')
  image = MIMEImage(fp.read(), filename)
  fp.close()
  msg.attach(image)

  # The actual mail send
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, toaddr, msg.as_string())
  server.quit()


sendMail("Waterlevel", "Waterlevel: " + filenamePic, filenamePic)
