# smarthome
Do every minute
+-temperature.sh
  +-create file name with date
   -read temp sensors
   -write csv file
   -write temperature values to web page
   -copy index.html to /var/www/
   -notify.py send mail if temperature in Vorlauf is higher than threshold
    +-read a list of last temperatures values from csv file
     -check if first element in temperature value list is higher or lower than threshold
     -send mail if lower or higher
   -LcdAny.bin sets temperature on display

+-waterlevel.sh
 +-create filename with date
  -read waterlevel with readSpiCh0mcp3008.bin
  -write waterlevel to csv file
  -waterlevelNotify.py checks waterlevel and sends mail (uses waterlevelTools.py)
   +-read last waterlevel values from csv file
    -analyse if waterlevel is rising or falling (trend) based on value stored in temp file
    -if trend is stable do nothing
    -calculate the current threshold based on the trend
    -rais or clear alarm based on thresolds
    -store 
  -LcdAny.bin sets waterlevel on display
  -write waterlevel to to web page
  
  
Testing:
>python3 test_waterlevelTools.py #UnitTests for waterlevelNotify.py
>python3 waterlevelTester.py waterlevel_2025_11_24.gz #feeds the values from waterlevel_2025_11_24.gz into waterlevelNotify.py
