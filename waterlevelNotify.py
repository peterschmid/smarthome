#!/usr/bin/python

# This skrip sends warning mails based on detected water level matching defined thresholds.
# First implementation was based on the last few lines of the data.csv file
# Second implementation stores the last threshold in a temp file
import sys, subprocess
from sendMail import sendTextMail
from waterlevelTools import getTrend
from waterlevelTools import isTrendRising
from waterlevelTools import isTrendStable
from waterlevelTools import isTrendFalling
from waterlevelTools import calculateThreshold
from waterlevelTools import raisAlarm
from waterlevelTools import clearAlarm
from waterlevelTools import extractLevels
from waterlevelTools import toNumbers
from waterlevelTools import getStoredThreshold
from waterlevelTools import storeThreshold
from waterlevelTools import tail
from waterlevelTools import filterJumpsBigger10

if len(sys.argv) != 2:
    print("Use first Argument as data file name")
    sys.exit(0)
filenameData = str(sys.argv[1])

filenameStoreThreshold = "/tmp/waterlevelThreshold.txt"

valuesToCheck = 8
#[0]         [1]       [2]
#Date;       Time;     Level
#20.05.2017; 00:00:01; 62
posOfLevelInLine = 2
startingThreshold = 68

#+2 for header and current level
levelsStr =  extractLevels(tail(filenameData, valuesToCheck+2),posOfLevelInLine)
levels = toNumbers(levelsStr)
levels = filterJumpsBigger10(levels)

if len(levels)<=valuesToCheck:
  # exit programm, there are not enought values
  sys.exit(0)

# current water level is in last position
trend = getTrend(levels, getStoredThreshold(filenameStoreThreshold))

if isTrendStable(trend):
  # exit programm, there is nothing to do
  sys.exit(0)

levelThreshold = 0

if isTrendRising(trend):
  levelThreshold = calculateThreshold(levels[-1], True)

if isTrendFalling(trend):
  levelThreshold = calculateThreshold(levels[-1], False)

if (raisAlarm(levels, levelThreshold)):
#  print("Send Mail above " + str(levelThreshold))
#  print(levels)
  sendTextMail("Wasserwarnung " + str(levelThreshold) + "cm", "Achtung der Wasserpegel ist aktuell auf " + str(max(levels)) + "cm angestiegen!")
  # only store threshold if mail is sent successfully
  storeThreshold(filenameStoreThreshold, levelThreshold)

if (clearAlarm(levels, levelThreshold)):
#  print("Send Mail below " + str(levelThreshold))
#  print(levels)
  sendTextMail("Wasserentwarnung " + str(levelThreshold) + "cm", "Der Wasserpegel ist wieder unter " + str(min(levels)) + " cm gesunken.")
  # only store threshold if mail is sent successfully
  storeThreshold(filenameStoreThreshold, levelThreshold)

# clear stored threshold if water is low
if levels[-1] < (startingThreshold - 5):
  storeThreshold(filenameStoreThreshold, 0)
