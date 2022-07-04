#!/usr/bin/python

import sys
from sendMail import sendSingelTextMail

# read cmd line
if len(sys.argv) != 2:
    # Wrong argument
    sendSingelTextMail("Wasserlevel Fehler!", "Achtung, es wurde kein Messwert gelesen!")
    sys.exit(0)

waterlevel  = 0
try:
    waterlevel = int(sys.argv[1])
except ValueError:
    # Handle the exception
    sendSingelTextMail("Wasserlevel Fehler!", "Achtung, der Messwert (" +str(sys.argv[1])+ ") konnte nicht gelesen werden!")

# check value
if waterlevel < 50 or waterlevel > 160:
    sendSingelTextMail("Wasserlevel Fehler!", "Achtung, der gelesene Messwert (" +str(waterlevel)+ ") ist nicht im Bereich >50 <160!")
else:
    print("All OK: " + str(waterlevel))
