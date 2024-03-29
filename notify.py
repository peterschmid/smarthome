#!/usr/bin/python

import sys, subprocess
from sendMail import sendSingelTextMail

if len(sys.argv) != 2:
    print("Use first Argument as data file name")
    sys.exit(0)
filenameData = str(sys.argv[1])

def tail( filename, lines=20 ):
    output = subprocess.check_output(['tail', '-n', str(lines), filename])
    return output.decode('ascii')

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
    #print (line)
    elementsOfLine = line.split(';')
    if len(elementsOfLine) > pos:
        values.append(elementsOfLine[pos])
  return values

def raisAlarm(tempList, threshold):
  #print(tempList)
  # check if only oldest value is lower
  if tempList[0]>=threshold:
    return False
  return all(i>=threshold for i in tempList[1:])

def clearAlarm(tempList, threshold):
  # check if only newest value is lower
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
#print (temp)
#print (raisAlarm(temp, tempThreshold))
#print (clearAlarm(temp, tempThreshold))
alarm = len(temp)>valuesToCheck and raisAlarm(temp, tempThreshold)
if alarm:
  #print("Send Mail")
  sendSingelTextMail("Temperatur Warnung", "Achtung die Temperatur im Vorlauf ist " + str(max(temp)) + " Grad.")

if (len(temp)>valuesToCheck and clearAlarm(temp, tempThreshold)):
  sendSingelTextMail("Temperatur Entwarnung", "Die Temperatur im Vorlauf ist wieder unter " + str(tempThreshold) + " Grand gesunken.")
