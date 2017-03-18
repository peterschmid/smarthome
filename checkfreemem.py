#!/usr/bin/python

import os, sys, smtplib

def getFreeMemInBytes():
  statvfs = os.statvfs('/home')
  #statvfs.f_frsize * statvfs.f_bfree      # Actual number of free bytes
  return  statvfs.f_frsize * statvfs.f_bavail

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

freeBytes = getFreeMemInBytes()
# send warning mail if free mem less than 1GB
if freeBytes < 1000000000:
  sendMail("Out of Memory Warning!", "Actual free memory is: "+str(freeBytes)+" Bytes")

