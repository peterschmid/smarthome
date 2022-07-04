#!/usr/bin/python

import sys
from sendMail import sendSingleTextMailWithPic
from email.message import EmailMessage


if len(sys.argv) != 2:
    print ("Use first Argument as picture file name")
    sys.exit(0)
filenamePic = str(sys.argv[1])

#print (filenameData)

sendSingleTextMailWithPic("Waterlevel", "Waterlevel: " + filenamePic, filenamePic)
