#!/usr/bin/python

# This skrip sends warning mails based on detected water level matching defined thresholds.
# First implementation was based on the last few lines of the data.csv file
# Second implementation stores the last threshold in a temp file
import sys, subprocess
from sendMail import sendTextMail

if len(sys.argv) != 2:
    print("Use first Argument as data file name")
    sys.exit(0)
filenameData = str(sys.argv[1])

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

def tail( filename, lines=20 ):
    output = subprocess.check_output(['tail', '-n', str(lines), filename])
    return output.decode('ascii')

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
  thresholds = [[70,65],[80,75],[90,85],[100,95],[110,105],[120,115],[130,125],[140,135],[150,145],[160,155],[170,165]]
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
  #print("Send Mail above " + str(levelThreshold))
  sendTextMail("Wasserwarnung " + str(levelThreshold) + "cm", "Achtung der Wasserpegel ist aktuell auf " + str(max(levels)) + "cm angestiegen!")
  # only store threshold if mail is sent successfully
  storeThreshold(levelThreshold)

if (len(levels)>valuesToCheck and clearAlarm(levels, levelThreshold)):
  #print("Send Mail below " + str(levelThreshold))
  sendTextMail("Wasserentwarnung " + str(levelThreshold) + "cm", "Der Wasserpegel ist wieder unter " + str(min(levels)) + " cm gesunken.")
  # only store threshold if mail is sent successfully
  storeThreshold(levelThreshold)

# clear stored threshold if water is low
if levels[-1] < (startingThreshold - 5):
  storeThreshold(0)
