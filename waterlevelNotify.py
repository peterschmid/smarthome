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

  # Create message
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

def extractLevel(text, pos):
  lines = text.split('\n')
  values = []
  for line in lines:
    # fails if LF is at end of file
    values.append(line.split(';')[pos]) 
  return values

def raisAlarm(valList, threshold):
  # check if only new values are higher
  if valList[0]>=threshold:
    return False
  return all(i>=threshold for i in valList[1:])

def clearAlarm(valList, threshold):
  # check if only new value is lower
  if valList[-1]>=threshold:
    return False
  return all(i>=threshold for i in valList[0:-1])

def calculateThreshold(level):
  # calcualte threshold based on level
  threshold = 70
  # threshold array [fixLevel,newThreshold]
  thresholds = [[75,80],[85,90],[95,100],[105,110],[115,120],[125,130],[135,140],[145,150],[155,160],[165,170]]
  for values in thresholds:
    if level > values[0]:
       threshold = values[1]
  return threshold

valuesToCheck = 3
#[0]         [1]       [2]
#Date;       Time;     Level
#20.05.2017; 00:00:01; 62
posOfLevelInLine = 2

#+2 for header and current level 
levelsStr =  extractLevel(tail(filenameData, valuesToCheck+2),posOfLevelInLine)
levels = toNumbers(levelsStr)
# last level is in last position
levelThreshold = calculateThreshold(levels[-1])

#print levelThreshold
#print levels
if (len(levels)>valuesToCheck and raisAlarm(levels, levelThreshold)):
  #print "Send Mail above " + str(levelThreshold)
  sendMail("Wasser Warnung " + str(levelThreshold) + "cm", "Achtung der Wasserpegel ist aktuell auf " + str(max(levels)) + "cm angestiegen!")

if (len(levels)>valuesToCheck and clearAlarm(levels, levelThreshold)):
  #print "Send Mail below " + str(levelThreshold)
  sendMail("Wasser Entwarnung " + str(levelThreshold) + "cm", "Der Wasserpegel ist wieder unter " + str(min(levels)) + " cm gesunken.")
