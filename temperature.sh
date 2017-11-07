#!/bin/bash

DATE=$(date +'%Y_%m_%d')
DATETIME=$(date +'%d.%m.%Y;%H:%M:%S')
FILENAME="logfile_$DATE.csv"
if [ ! -f $FILENAME ]
then
    echo "Date;Time;AirIn;AirOut;FloorIn;FloorOut;SolarUp;SolarDown;WarmWater;FloorIn2" > $FILENAME
fi

TEMP_AIR_IN=$( echo "scale=3; $( grep 't=' /sys/bus/w1/devices/10-000802b5b23a/w1_slave | awk -F 't=' '{print $2}') / 1000" | bc -l)
TEMP_AIR_OUT=$( echo "scale=3; $( grep 't=' /sys/bus/w1/devices/10-000802b5cf94/w1_slave | awk -F 't=' '{print $2}') / 1000" | bc -l)
TEMP_FLOOR_IN=$( echo "scale=3; $( grep 't=' /sys/bus/w1/devices/10-000802b5c6b8/w1_slave | awk -F 't=' '{print $2}') / 1000" | bc -l)
TEMP_FLOOR_OUT=$( echo "scale=3; $( grep 't=' /sys/bus/w1/devices/10-000802ddfe20/w1_slave | awk -F 't=' '{print $2}') / 1000" | bc -l)
TEMP_SOL_UP=$( echo "scale=3; $( grep 't=' /sys/bus/w1/devices/10-000802b5ea69/w1_slave | awk -F 't=' '{print $2}') / 1000" | bc -l)
TEMP_SOL_DOWN=$( echo "scale=3; $( grep 't=' /sys/bus/w1/devices/10-000802de6015/w1_slave | awk -F 't=' '{print $2}') / 1000" | bc -l)
TEMP_WARM_WATER=$( echo "scale=3; $( grep 't=' /sys/bus/w1/devices/10-000802e73212/w1_slave | awk -F 't=' '{print $2}') / 1000" | bc -l)
TEMP_FLOOR_IN_2=$( echo "scale=3; $( grep 't=' /sys/bus/w1/devices/10-000802de52c6/w1_slave | awk -F 't=' '{print $2}') / 1000" | bc -l)

#echo "$TEMP_AIR_IN $TEMP_AIR_OUT $TEMP_FLOOR_IN $TEMP_FLOOR_OUT $TEMP_SOL_UP $TEMP_SOL_DOWN"
#echo "$FILENAME"
#write temperatures to csv file
echo "$DATETIME;$TEMP_AIR_IN;$TEMP_AIR_OUT;$TEMP_FLOOR_IN;$TEMP_FLOOR_OUT;$TEMP_SOL_UP;$TEMP_SOL_DOWN;$TEMP_WARM_WATER;$TEMP_FLOOR_IN_2" >> $FILENAME

#create html table
HTMLTABLE="<table style=\"width:100%\"> <tr><td>FloorIn</td><td>$TEMP_FLOOR_IN</td></tr> <tr><td>FloorOut</td><td>$TEMP_FLOOR_OUT</td></tr> <tr><td>SolarUp</td><td>$TEMP_SOL_UP</td></tr>  <tr><td>SolarDown</td><td>$TEMP_SOL_DOWN</td></tr>  <tr><td>WarmWater</td><td>$TEMP_WARM_WATER</td></tr>  </table>"

#echo "$HTMLTABLE"

#update html table
sed -i '3d' index.html
sed -i "3i\
$HTMLTABLE
" index.html
#copy homepage
cp index.html /var/www/

# send mail
./notify.py $FILENAME

# write to display
./LcdAny.bin 2 Vorlauf $TEMP_FLOOR_IN_2 C
