#!/usr/bin/python

# This skrip sends warning mails based on detected water level matching defined thresholds.
# First implementation was based on the last few lines of the data.csv file
# Second implementation stores the last threshold in a temp file
import sys, subprocess, math

def getStoredThreshold(filenameStoreThreshold):
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

def storeThreshold(filenameStoreThreshold, threshold):
  f=open(filenameStoreThreshold, "w+")
  f.write(str(threshold))
  f.close()

def tail(filename, lines=20):
    try:
        output = subprocess.check_output(['tail', '-n', str(lines), filename])
    except subprocess.CalledProcessError:
        return ('')
    return output.decode('ascii')

def toNumbers(values):
    values2 = []
    for val in values:
      try:
        values2.append(float(val))
      except ValueError:
        pass
    return values2

def roundUpOrDown(avg, val):
    if val < avg:
        return math.floor(avg)
    if val > avg:
        return math.ceil(avg)
    return avg 
    
def filterJumpsBigger10(values):
    diff = 10.0
    values2 = []
    if len(values) > 3:
        avg = sum(values) / float(len(values))
        for val in values[0:-1]:
            if abs(val-avg) >= diff:
                values2.append(roundUpOrDown(avg, val))
            else:
                values2.append(val)
        if abs(values[-1]-values[-2]) >= diff:
            values2.append(roundUpOrDown(avg, val))
        else:
            values2.append(values[-1])
        return values2
    return values

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

def calculateThreshold(levels, isTrendRising):
  # calcualte threshold based on levels
  # threshold array [rising threshold, falling threshold]
  thresholds = [[70,65],[80,75],[90,85],[100,95],[110,105],[120,115],[130,125],[140,135],[150,145],[160,155],[170,165]]
  avg = sum(levels)/float(len(levels))
  if isTrendRising:
    threshold = thresholds[-1][0]
    for values in reversed(thresholds):
      if avg <= values[0]:
        threshold = values[0]
  else:
    threshold = thresholds[0][1]
    for values in thresholds:
      if avg >= values[1]:
        threshold = values[1]
  return threshold

def getTrend(valList, lastThreshold):
  #-1 is falling, 0 stable, +1 rising
  # current level is last in list
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
    if valList[-1] > math.ceil(avg):
      return 1
    elif valList[-1] < math.floor(avg):
      return -1
    else:
      return 0

def isTrendStable(trend):
   return trend == 0

def isTrendFalling(trend):
  return trend == -1

def isTrendRising(trend):
  return trend == 1

	
