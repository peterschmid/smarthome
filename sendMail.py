import os, smtplib, imghdr, email.utils
from email.message import EmailMessage
import configparser


def readCofnigFile(configfilename):
  """This function reads the given config file and returns the values
     [Server]
     smtpserver: serveradr.com
     port: 465
     usr: mymail@serveradr.com
     pw: password
     [Destination]
     toaddr1: anymail@any.com
     toaddr2: anymail@any.com
     ...

     @return smtpServer, port, usr, pw, toaddr[]
  """
  config = configparser.ConfigParser()
  config.read(configfilename)
  serverSection = 'Server'
  destiantonSection = 'Destination'
  smtpServer = 'smtpserver'
  port       = 'port'
  usr        = 'usr'
  pw         = 'pw'
  toaddrList = []
 
  if not os.path.isfile(configfilename):
    print('Cofig File missing')
    return smtpServer, port, usr, pw, toaddrList

  if serverSection in config:
    if smtpServer in config[serverSection]:
      smtpServer = config.get(serverSection, smtpServer)
    else:
      print('Cofig File missing value: ' + smtpServer)
    if port in config[serverSection]:
      port       = config.get(serverSection, port)
    else:
      print('Cofig File missing value: ' + port)
    if usr in config[serverSection]:
      usr        = config.get(serverSection, usr)
    else:
      print('Cofig File missing value: ' + usr)
    if pw in config[serverSection]:
      pw         = config.get(serverSection, pw)
    else:
      print('Cofig File missing value: ' + pw)
  else:
    print('Cofig File missing section: ' + serverSection)

  if destiantonSection in config:
    for key in config[destiantonSection]:
      toaddrList.append(config.get(destiantonSection, key))
    if not toaddrList:
      print('Cofig File missing value in section: ' + serverSection)
  else:
    print('Cofig File missing section: ' + destiantonSection)
  return smtpServer, port, usr, pw, toaddrList

def sendMail(smtpServer='', port='', usr='', pw='', toaddrList=[''], subject='TestMail' , body='This is a Test', filenameAttachPic = ''):
  fromaddr = usr

  # Create the root message and fill in the from, to, and subject headers
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = fromaddr
  msg['To'] = toaddrList[0]
  msg['Date'] = email.utils.formatdate(localtime=True)
  msg.set_content(body)

  if filenameAttachPic: 
    fp = open(filenameAttachPic, 'rb')
    image = fp.read()
    fp.close()
    msg.add_attachment(image, maintype='image', subtype=imghdr.what(None, image), filename=filenameAttachPic)

  # The actual mail send
  server = smtplib.SMTP_SSL(host=smtpServer, port=port)  
  server.login(usr,pw)
  for toaddr in toaddrList:
    msg.replace_header('To', toaddr)
    server.sendmail(fromaddr, toaddr, msg.as_string())
  server.quit()


def sendSingelTextMail(subject, body):
  smtpServer, port, usr, pw, toaddrList =  readCofnigFile('mail.conf')
  sendMail(smtpServer, port, usr, pw, toaddrList[0:1], subject, body)

def sendTextMail(subject, body):
  smtpServer, port, usr, pw, toaddrList =  readCofnigFile('mail.conf')
  sendMail(smtpServer, port, usr, pw, toaddrList, subject, body)

def sendSingleTextMailWithPic(subject, body, filenameAttachPic):
  smtpServer, port, usr, pw, toaddrList =  readCofnigFile('mail.conf')
  sendMail(smtpServer, port, usr, pw, toaddrList[0:1], subject, body, filenameAttachPic)

