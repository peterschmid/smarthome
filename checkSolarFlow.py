#!/usr/bin/python
import sys, smtplib, subprocess

if len(sys.argv) != 2:
    print("Use first Argument as data file name")
    sys.exit(0)
filenameData = str(sys.argv[1])

# Read file with format: from address, password, to address
def getMailData():
  l = []
  with open("mail.txt", "r") as f:
    lines = (line.strip() for line in f) # All lines including the blank ones
    lines = (line for line in lines if line) # Non-blank lines
    l = list(lines) # convert generator to list
  return l[0], l[1], l[2]

filenameStoreThreshold = "/tmp/waterlevelThreshold.txt"

def getStoredThreshold():
  lastThreshold = 0;
  try:
    f=open(filenameStoreThreshold, "r")
    content = f.readline()
    f.close()
    try:
      lastThreshold = int(content)
    except ValueError:
      pass
  except IOError:
    pass
  return lastThreshold

def sendMail(sub, text):
  # Prepare sending Mail and credentians
  fromaddr, password, toaddr =  getMailData()
  username = fromaddr

  # Create message
  msg = 'Subject: %s\n\n%s' % (sub, text)

  # The actual mail send
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, toaddr, msg)
  server.quit()

def tail( filename, lines=20 ):
    output = subprocess.check_output(['tail', '-n', str(lines), filename])
    return output.decode('ascii')

def toNumbers(values):
    values2 = []
    for val in values:
      try:
        values2.append(float(val))
      except ValueError:
        pass
    return values2

def extractValues(text, pos):
  lines = text.split('\n')
  values = []
  for line in lines:
    if line:
      splitLine = line.split(';')
      if len(splitLine)-1 < pos:
        print("Error accessing index " + str(pos) +" in list, Content: " + line)
      else: 
        values.append(splitLine[pos]) 
  return values

# last 60 values (1h of data)
valuesToCheck = 60
waringThreshold = 3

#[0]         [1]       [2]     [3]     [4]      [5]       [6]      [7]
#Date;       Time;     AirIn;  AirOut; FloorIn; FloorOut; SolarUp; SolarDown; WarmWate$
#16.09.2020; 00:00:01; 23.562; 23.875; 29.687;  28.187;   23.500;  23.812;    65.937; $
positionOfSolarUpInLine = 6
positionOfSolarDownInLine = 7

#+2 for header and current data
solarUpStr   = extractValues(tail(filenameData, valuesToCheck+2),positionOfSolarUpInLine)
solarDownStr = extractValues(tail(filenameData, valuesToCheck+2),positionOfSolarDownInLine)

solarUp   = toNumbers(solarUpStr)
solarDown = toNumbers(solarDownStr)

avgSolarUp   = sum(solarUp)/len(solarUp)
avgSolarDown = sum(solarDown)/len(solarDown)

#print("Detected Temp diff between avgSolUp and avgSolDown: " + str(avgSolarUp - avgSolarDown))

# if difference between up and down average is higher than 3 degrade Celsius
if (avgSolarUp - avgSolarDown) > waringThreshold:
  #print("Temp diff detected in file: " + filenameData)
  #send mail
  sendMail("Warning: Solar flow blocked", "Average temp up is warmer than average temp down. Go check the flow meter, it's possibly jamed.")

