#!/usr/bin/python

import sys, smtplib

def readFromMailAdrAndPwAndToMailAdr():
  f=open("mail.txt", "r")
  content = f.readlines()
  content = [x.strip('\n') for x in content]
  return content[0], content[1], content[2]

def sendMail(sub, text):
  # Prepare sending Mail and credentians
  fromaddr, password, toaddr =  readFromMailAdrAndPwAndToMailAdr()
  username = fromaddr

  msg = 'Subject: %s\n\n%s' % (sub, text)

  # The actual mail send
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, toaddr, msg)
  server.quit()

# read cmd line
if len(sys.argv) != 2:
    # Wrong argument
    sendMail("Wasserlevel Fehler!", "Achtung, es wurde kein Messwert gelesen!")
    sys.exit(0)

waterlevel  = 0
try:
    waterlevel = int(sys.argv[1])
except ValueError:
    # Handle the exception
    sendMail("Wasserlevel Fehler!", "Achtung, der Messwert (" +str(sys.argv[1])+ ") konnte nicht gelesen werden!")

# check value
if waterlevel < 50 or waterlevel > 160:
    sendMail("Wasserlevel Fehler!", "Achtung, der gelesene Messwert (" +str(waterlevel)+ ") ist nicht im Bereich >50 <160!")
else:
    print("All OK: " + str(waterlevel))
