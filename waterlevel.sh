#!/bin/bash

DATE=$(date +'%Y_%m_%d')
DATETIME=$(date +'%d.%m.%Y;%H:%M:%S')
FILENAME="waterlevel_$DATE.csv"

#print header if file not existing
if [ ! -f $FILENAME ]
then
    echo "Date;Time;Level" > $FILENAME
fi

#call SPI bin and store return code
#LEVEL_CM=$(echo $(./OutBinStub))
LEVEL_CM=$(echo $(./readSpiCh0mcp3008.bin))

#write level to csv file if not empty
if [ -n "$LEVEL_CM" ]; then
    echo "$DATETIME;$LEVEL_CM" >> $FILENAME
fi

# check level and send mail
./waterlevelNotify.py $FILENAME

# send value to display
./LcdAny.bin 1 Wasserstand $LEVEL_CM cm

#send level value to ubidots skript
#./sendtoubidots.py $LEVEL_CM
