#!/usr/bin/python

import sys, smtplib

if len(sys.argv) != 2:
    print "Use first Argument as data file name"
    sys.exit(0)
filenameData = str(sys.argv[1])

#print filenameData

def readFromMailAdrAndPwAndToMailAdr():
  f=open("mail.txt", "r")
  content = f.readlines()
  content = [x.strip('\n') for x in content]
  return content[0], content[1], content[2]

def sendMail(sub, text):
  # Prepare sending Mail and credentians
  fromaddr, password, toaddr =  readFromMailAdrAndPwAndToMailAdr()
  username = fromaddr

  #sub = 'Temperaturwarung'
  #text = 'Die Temperatur ist zu hoch!'
  msg = 'Subject: %s\n\n%s' % (sub, text)

  # The actual mail send
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, toaddr, msg)
  server.quit()

def tail( filename, lines=20 ):
    total_lines_wanted = lines

    f = open(filename, "r")
    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

def toNumbers(values):
    values2 = []
    for val in values:
      try:
        values2.append(float(val))
      except ValueError:
        continue
    return values2

def extractTemp(text, pos):
  lines = text.split('\n')
  values = []
  for line in lines:
    # fails if LF is at end of file
    values.append(line.split(';')[pos]) 
  return values

def raisAlarm(tempList, threshold):
  print tempList
  # check if only new values are higher
  if tempList[-1]<=threshold:
    return False
  return all(i<=threshold for i in tempList[0:-1])

def clearAlarm(tempList, threshold):
  if tempList[-1]>=threshold:
    return False
  return all(i>=threshold for i in tempList[0:-1])

valuesToCheck = 5
#[0]         [1]       [2]     [3]     [4]      [5]       [6]      [7]        [8]        [9]
#Date;       Time;     AirIn;  AirOut; FloorIn; FloorOut; SolarUp; SolarDown; WarmWater; FloorIn2
#09.05.2016; 00:00:01; 20.812; 20.812; 23.125;  21.562;   18.750;  18.750;    56.562;    23.062
posOfFloorInValue = 9
tempThreshold = 40

tempStr =  extractTemp(tail(filenameData, valuesToCheck +3),posOfFloorInValue)
temp = toNumbers(tempStr)
alarm = len(temp)>valuesToCheck and raisAlarm(temp, tempThreshold)
if alarm:
  #print "Send Mail"
  sendMail("Temperatur Warnung", "Achtung die Temperatur im Vorlauf ist " + str(max(temp)) + " Grad.")

if (len(temp)>valuesToCheck and clearAlarm(temp, tempThreshold)):
  sendMail("Temperatur Entwarnung", "Die Temperatur im Vorlauf ist wieder unter " + str(tempThreshold) + " Grand gesunken.")
