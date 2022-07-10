#!/usr/bin/python

import unittest
import configparser
import os
from sendMail import readCofnigFile

testfilename = 'test.conf'

class TestConfigReader(unittest.TestCase):

  def setUp(self):
    super(TestConfigReader, self).setUp()
    if os.path.isfile(testfilename):
      os.remove(testfilename) 

  def tearDown(self):
    if os.path.isfile(testfilename):
      os.remove(testfilename) 

  def test_configparserAllOk(self):
    config = configparser.ConfigParser()
    config['Server'] = {'smtpserver': 'mail.com', 'port': '1', 'usr': 'tester', 'pw': 'top secret'}
    config['Destination'] = {'adr1': 'test1@test.com', 'adr2': 'test2@test.com'} 
    with open(testfilename, 'w') as configfile:
      config.write(configfile)

    smtpServer, port, usr, pw, toaddr = readCofnigFile('test.conf')

    self.assertEqual(smtpServer, 'mail.com', "Should be mail.com")
    self.assertEqual(port, '1', "Should be 1")
    self.assertEqual(usr, 'tester', "Should be tester")
    self.assertEqual(pw, 'top secret', "Should be top secret")
    self.assertEqual(toaddr, ['test1@test.com', 'test2@test.com'])

  def test_configparserNoPw(self):
    config = configparser.ConfigParser()
    config['Server'] = {'smtpserver': 'mail.com', 'port': '1', 'usr': 'tester'}
    config['Destination'] = {'adr1': 'test1@test.com', 'adr2': 'test2@test.com'} 
    with open(testfilename, 'w') as configfile:
      config.write(configfile)

    smtpServer, port, usr, pw, toaddr = readCofnigFile('test.conf')

    self.assertEqual(smtpServer, 'mail.com', "Should be mail.com")
    self.assertEqual(port, '1', "Should be 1")
    self.assertEqual(usr, 'tester', "Should be tester")
    self.assertEqual(pw, 'pw', "Should be top secret")
    self.assertEqual(toaddr, ['test1@test.com', 'test2@test.com'])

  def test_configparserWrongServerSection(self):
    config = configparser.ConfigParser()
    config['WrongServer'] = {'smtpserver': 'mail.com', 'port': '1', 'usr': 'tester', 'pw': 'top secret'}
    config['Destination'] = {'adr1': 'test1@test.com', 'adr2': 'test2@test.com'} 
    with open(testfilename, 'w') as configfile:
      config.write(configfile)

    smtpServer, port, usr, pw, toaddr = readCofnigFile('test.conf')

    self.assertEqual(smtpServer, 'smtpserver', "Should be smtpserver")
    self.assertEqual(port, 'port', "Should be port")
    self.assertEqual(usr, 'usr', "Should be usr")
    self.assertEqual(pw, 'pw', "Should be top secret")
    self.assertEqual(toaddr, ['test1@test.com', 'test2@test.com'])

  def test_configparserWrongDestinationSection(self):
    config = configparser.ConfigParser()
    config['Server'] = {'smtpserver': 'mail.com', 'port': '1', 'usr': 'tester', 'pw': 'top secret'}
    config['WrongDestination'] = {'adr1': 'test1@test.com', 'adr2': 'test2@test.com'} 
    with open(testfilename, 'w') as configfile:
      config.write(configfile)

    smtpServer, port, usr, pw, toaddr = readCofnigFile('test.conf')

    self.assertEqual(smtpServer, 'mail.com', "Should be mail.com")
    self.assertEqual(port, '1', "Should be 1")
    self.assertEqual(usr, 'tester', "Should be tester")
    self.assertEqual(pw, 'top secret', "Should be top secret")
    self.assertEqual(toaddr, [])

  def test_configparserNoCofnigFile(self):
    smtpServer, port, usr, pw, toaddr = readCofnigFile('test.conf')

    self.assertEqual(smtpServer, 'smtpserver', "Should be smtpserver")
    self.assertEqual(port, 'port', "Should be port")
    self.assertEqual(usr, 'usr', "Should be usr")
    self.assertEqual(pw, 'pw', "Should be pw")
    self.assertEqual(toaddr, [])

if __name__ == '__main__':
    unittest.main()


#.assertEqual(a, b) 	a == b
#.assertTrue(x) 	bool(x) is True
#.assertFalse(x) 	bool(x) is False
#.assertIs(a, b) 	a is b
#.assertIsNone(x) 	x is None
#.assertIn(a, b) 	a in b
#.assertIsInstance(a, b) 	isinstance(a, b)
