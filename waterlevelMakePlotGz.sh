#! /bin/bash
DATE=$(date +'%Y_%m_%d' --date='yesterday')
FILENAME="waterlevel_$DATE"
INFILE="$FILENAME.csv"
OUTFILE="$FILENAME.png"
GZFILE="$FILENAME.gz"
TITLE="Waterlevel [cm] $DATE"


#echo $INFILE
export infile=$INFILE
export outfile=$OUTFILE
export titlename=$TITLE

#check if there was water
./waterlevelThresholdFinder.py $INFILE
if [ $? == 0 ]
then
    # there was water, make plot and zip values
    ./waterlevelMakePlot.gnp && \
    tar -cjf $GZFILE $INFILE --remove-files

    # send graph via e-mail
    ./waterlevelSendPic.py $OUTFILE

    # move picture to web dir
    mv $OUTFILE /var/www/graph/

    # write web page
    sed -i "40i\
    <p><img src=\"graph/$OUTFILE\" alt=\"$DATE\"></p>
    " index.html
    cp index.html /var/www/
else
    # gzip
    tar -cjf $GZFILE $INFILE --remove-files
fi
