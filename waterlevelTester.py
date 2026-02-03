#!/usr/bin/python

# Reades given tar bz2 file line by line. One by one the lines are written to a
# temp file, which is passed to the test programm 
import sys, tarfile, tempfile, os

if len(sys.argv) != 2:
    print ("Use first Argument as test data file name (gz)")
    sys.exit(0)
filenameTestData = str(sys.argv[1])

# open tar/bz2 file and walk through
tar = tarfile.open(filenameTestData, "r:bz2")
for tarinfo in tar:
    testDataFile = tar.extractfile(tarinfo.name)
    # create temp file
    tempFile = tempfile.NamedTemporaryFile(mode='a');
    doFirstWriteHeader = True
    # add each line to temp file
    for line in testDataFile:
        line = line.decode('utf-8')
        if doFirstWriteHeader:
            # write only header to file
            tempFile.write(str(line))
            doFirstWriteHeader = False
        else:
            # go to end of file (needed to ensure proper file handling)
            tempFile.seek(0,2)
            tempFile.write(str(line))
            # go to start of file (needed to ensure proper file handling)
            tempFile.seek(0)
            # call the program to test
            #print ("python3 waterlevelNotify.py" + " " + tempFile.name)
            ret = os.system("python3 waterlevelNotify.py" + " " + tempFile.name)
            #os.system("tail" + " " + tempFile.name)
            if ret != 0:
                print (line)
        #input()

# clean up
tar.close()
tempFile.close()
