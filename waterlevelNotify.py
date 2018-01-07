#!/usr/bin/python

# This skrip sends warning mails based on detected water level matching defined thresholds.
# First implementation was based on the last few lines of the data.csv file
# Second implementation stores the last threshold in a temp file
import sys, smtplib

if len(sys.argv) != 2:
    print "Use first Argument as data file name"
    sys.exit(0)
filenameData = str(sys.argv[1])

# Read file with format: from address, password, to address1, to address2...
def getMailData():
  l = []
  with open("mail.txt", "r") as f:
    lines = (line.strip() for line in f) # All lines including the blank ones
    lines = (line for line in lines if line) # Non-blank lines
    l = list(lines) # convert generator to list
  return l[0], l[1], l[2:]

filenameStoreThreshold = "/tmp/waterlevelThreshold.txt"

def getStoredThreshold():
  lastThreshold = 0;
  try:
    f=open(filenameStoreThreshold, "r")
    content = f.readline()
    f.close()
    try:
      lastThreshold = int(content)
    except ValueError:
      pass
  except IOError:
    pass
  return lastThreshold

def storeThreshold(threshold):
  f=open(filenameStoreThreshold, "w+")
  f.write(str(threshold))
  f.close()

def sendMail(sub, text):
  # Prepare sending Mail and credentians
  fromaddr, password, toaddrList =  getMailData()
  username = fromaddr

  # Create message
  msg = 'Subject: %s\n\n%s' % (sub, text)

  # The actual mail send
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  for toaddr in toaddrList:
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
        pass
    return values2

def extractLevels(text, pos):
  lines = text.split('\n')
  values = []
  for line in lines:
    if line:
        values.append(line.split(';')[pos]) 
  return values

def raisAlarm(valList, threshold):
  # check if only new values are higher
  if valList[-1]<threshold:
    return False
  return all(i<threshold for i in valList[0:-1])

def clearAlarm(valList, threshold):
  # check if only new value is lower
  if valList[-1]>threshold:
    return False
  return all(i>threshold for i in valList[0:-1])

def calculateThreshold(level, isTrendRising):
  # calcualte threshold based on level
  threshold = startingThreshold
  # threshold array [rising threshold, falling threshold]
  thresholds = [[80,75],[90,85],[100,95],[110,105],[120,115],[130,125],[140,135],[150,145],[160,155],[170,165]]
  if isTrendRising:
    for values in thresholds:
      if level >= values[0]:
        threshold = values[0]
  else:
    for values in reversed(thresholds):
      if level <= values[1]:
        threshold = values[1]
  return threshold

def getTrend(valList):
  #-1 is falling, 0 stable, +1 rising
  # current level is last in list
  lastThreshold = getStoredThreshold()
  if lastThreshold > 0:
    # lastThreshold could be read, use it for trend
    blurFactor = 2
    if valList[-1] > (lastThreshold + blurFactor):
      return 1
    elif valList[-1] < (lastThreshold - blurFactor):
      return -1
    else:
      return 0
  else:
    # get trend from varList
    avgList = valList[0:-1]
    avg = 1
    if avgList:
      avg = sum(avgList)/float(len(avgList))
    if valList[-1] > avg:
      return 1
    elif valList[-1] < avg:
      return -1
    else:
      return 0

def isTrendStable(trend):
   return trend == 0

def isTrendFalling(trend):
  return trend == -1

def isTrendRising(trend):
  return trend == 1

valuesToCheck = 3
#[0]         [1]       [2]
#Date;       Time;     Level
#20.05.2017; 00:00:01; 62
posOfLevelInLine = 2
startingThreshold = 70

#+2 for header and current level
levelsStr =  extractLevels(tail(filenameData, valuesToCheck+2),posOfLevelInLine)
levels = toNumbers(levelsStr)

# current water level is in last position
trend = getTrend(levels)

if isTrendStable(trend):
  # exit programm, there is nothing to do
  sys.exit(0)

levelThreshold = 0

if isTrendRising(trend):
  levelThreshold = calculateThreshold(levels[-1], True)

if isTrendFalling(trend):
  levelThreshold = calculateThreshold(levels[-1], False)

if (len(levels)>valuesToCheck and raisAlarm(levels, levelThreshold)):
  #print "Send Mail above " + str(levelThreshold)
  sendMail("Wasser Warnung " + str(levelThreshold) + "cm", "Achtung der Wasserpegel ist aktuell auf " + str(max(levels)) + "cm angestiegen!")
  # only store threshold if mail is sent successfully
  storeThreshold(levelThreshold)
  
if (len(levels)>valuesToCheck and clearAlarm(levels, levelThreshold)):
  #print "Send Mail below " + str(levelThreshold)
  sendMail("Wasser Entwarnung " + str(levelThreshold) + "cm", "Der Wasserpegel ist wieder unter " + str(min(levels)) + " cm gesunken.")
  # only store threshold if mail is sent successfully
  storeThreshold(levelThreshold)

# clear stored threshold if water is low
if levels[-1] < (startingThreshold - 5):
  storeThreshold(0)
