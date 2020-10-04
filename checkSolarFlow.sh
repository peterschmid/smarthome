#!/bin/bash

DATE=$(date +'%Y_%m_%d')
DATETIME=$(date +'%d.%m.%Y;%H:%M:%S')
FILENAME="logfile_$DATE.csv"

# check solar flow and send mail if jamed
./checkSolarFlow.py $FILENAME
