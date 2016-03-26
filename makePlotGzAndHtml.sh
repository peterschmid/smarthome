#! /bin/bash
DATE=$(date +'%Y_%m_%d' --date='yesterday')
FILENAME="logfile_$DATE"
INFILE="$FILENAME.csv"
OUTFILE="$FILENAME.png"
GZFILE="$FILENAME.gz"
TITLE="Temperature $DATE"
#echo $INFILE
export infile=$INFILE
export outfile=$OUTFILE
export titlename=$TITLE
#make plot and zip values
./makePlot.gnp && \
tar -cjf $GZFILE $INFILE && \
rm $INFILE

# send graph via e-mail
./sendPic.py $OUTFILE

# move picture to web dir
mv $OUTFILE /var/www/graph/

# write web page
sed -i "4i\
<p><img src=\"graph/$OUTFILE\" alt=\"$DATE\"></p>
" index.html
#cp index.html /var/www/
