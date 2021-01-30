#!/bin/bash

#call SPI bin and store return code
#LEVEL_CM=$(echo $(./OutBinStub))
LEVEL_CM=$(echo $(./readSpiCh0mcp3008.bin))

#check value
./checkWaterlevel.py $LEVEL_CM

