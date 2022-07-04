#!/usr/bin/python

import os, sys
from sendMail import sendSingelTextMail

def getFreeMemInBytes():
  statvfs = os.statvfs('/home')
  #statvfs.f_frsize * statvfs.f_bfree      # Actual number of free bytes
  return  statvfs.f_frsize * statvfs.f_bavail


freeBytes = getFreeMemInBytes()
#print(freeBytes)
# send warning mail if free mem less than 1GB
if freeBytes < 1000000000:
  sendSingelTextMail("Out of Memory Warning!", "Actual free memory is: "+str(freeBytes)+" Bytes")

