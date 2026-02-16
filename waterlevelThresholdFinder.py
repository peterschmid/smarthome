#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print ("Use first Argument as data file name")
    sys.exit(1)
filenameData = str(sys.argv[1])

#print filenameData

threshold = 70

#read line by line and check if a value is above threshold
f=open(filenameData, "r")
for line in f:
    levelList = line.split(';')
    if 3 >= len(levelList):
        try:
            level = int(levelList[2])
            if threshold <= level:
                print ("Interesting")
                # exit with success
                sys.exit(0)
        except (ValueError):
            #no action
            pass
#exit with failure
sys.exit(1)


