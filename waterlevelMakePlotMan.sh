#! /bin/bash

#first agrument must be a date
if [ -z "$1" ]
then
    echo "Date is missing (Format: 2022_09_30)"
    exit 1
fi

if [ -z "$2" ]
then
    echo "Step is missing (1=do Plot, 2=do Plot,zip,move and html)"
    exit 1
fi

DATE=$1
FILENAME="waterlevel_$DATE"
INFILE="$FILENAME.csv"
OUTFILE="$FILENAME.png"
GZFILE="$FILENAME.gz"
TITLE="Waterlevel [cm] $DATE"


#echo $INFILE
export infile=$INFILE
export outfile=$OUTFILE
export titlename=$TITLE

# there was water, make plot and zip values
if [ "$2" == "1" ]
then
    echo "Make plot..."
    ./waterlevelMakePlot.gnp
fi

if [ "$2" == "2" ]
then
    echo "Make plot, zip and remove..."
    ./waterlevelMakePlot.gnp && \
    tar -cjf $GZFILE $INFILE --remove-files

    # move picture to web dir
    echo "...move file..."
    mv $OUTFILE /var/www/graph/

    # write web page
    echo "...create html entry.."
    sed -i "40i\<p><img src=\"graph/$OUTFILE\" alt=\"$DATE\"></p>" index.html
    #cp index.html /var/www/
fi

echo "...done!"
