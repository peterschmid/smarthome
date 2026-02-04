#!/usr/bin/python

import unittest
import os
from waterlevelTools import getTrend
from waterlevelTools import isTrendStable
from waterlevelTools import isTrendFalling
from waterlevelTools import isTrendRising
from waterlevelTools import calculateThreshold
from waterlevelTools import raisAlarm
from waterlevelTools import clearAlarm
from waterlevelTools import extractLevels
from waterlevelTools import toNumbers
from waterlevelTools import getStoredThreshold
from waterlevelTools import storeThreshold
from waterlevelTools import tail
from waterlevelTools import roundUpOrDown
from waterlevelTools import filterJumpsBigger10

class TestStringMethods(unittest.TestCase):

    def test_getTrend_lastT0_trendRising1(self):
        levels = [60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 61.0]
        lastThreshold = 0
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 1)
        self.assertTrue(isTrendRising(trend))
        self.assertFalse(isTrendFalling(trend))
        self.assertFalse(isTrendStable(trend))

    def test_getTrend_lastT0_trendRising2(self):
        levels = [61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 62.0]
        lastThreshold = 0
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 1)


    def test_getTrend_lastT0_trendStable1(self):
        levels = [60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0]
        lastThreshold = 0
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 0)
        self.assertTrue(isTrendStable(trend))
        self.assertFalse(isTrendFalling(trend))

    def test_getTrend_lastT0_trendStable2(self):
        levels = [61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0]
        lastThreshold = 0
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 0)
        self.assertTrue(isTrendStable(trend))

    def test_getTrend_lastT0_trendStable3(self):
        levels = [60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0]
        lastThreshold = 0
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 0)
        self.assertTrue(isTrendStable(trend))


    def test_getTrend_lastT0_trendFalling1(self):
        levels = [60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 59.0]
        lastThreshold = 0
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, -1)
        self.assertTrue(isTrendFalling(trend))
        self.assertFalse(isTrendStable(trend))

    def test_getTrend_lastT0_trendFalling2(self):
        levels = [60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 60.0, 61.0, 59.0]
        lastThreshold = 0
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, -1)
        self.assertTrue(isTrendFalling(trend))

    def test_getTrend_lastT70_trendRising1(self):
        levels = [80.0, 60.0, 80.0, 60.0, 80.0, 60.0, 60.0, 80.0, 60.0, 80.0, 73.0]
        lastThreshold = 70
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 1)

    def test_getTrend_lastT70_trendRising2(self):
        levels = [80.0, 60.0, 80.0, 60.0, 80.0, 60.0, 60.0, 80.0, 60.0, 80.0, 75.0]
        lastThreshold = 70
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 1)

    def test_getTrend_lastT70_trendStable1(self):
        levels = [80.0, 60.0, 80.0, 60.0, 80.0, 60.0, 60.0, 80.0, 60.0, 80.0, 72.0]
        lastThreshold = 70
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 0)

    def test_getTrend_lastT70_trendStable2(self):
        levels = [80.0, 60.0, 80.0, 60.0, 80.0, 60.0, 60.0, 80.0, 60.0, 80.0, 68.0]
        lastThreshold = 70
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, 0)

    def test_getTrend_lastT70_trendFalling1(self):
        levels = [80.0, 60.0, 80.0, 60.0, 80.0, 60.0, 60.0, 80.0, 60.0, 80.0, 67.0]
        lastThreshold = 70
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, -1)

    def test_getTrend_lastT70_trendFalling2(self):
        levels = [80.0, 60.0, 80.0, 60.0, 80.0, 60.0, 60.0, 80.0, 60.0, 80.0, 65.0]
        lastThreshold = 70
        trend = getTrend(levels, lastThreshold)
        self.assertEqual(trend, -1)


    def test_raisAlarm_OK1(self):
        valList = [69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 70.0]
        threshold = 70
        self.assertTrue(raisAlarm(valList, threshold))

    def test_raisAlarm_OK2(self):
        valList = [60.0, 60.0, 60.0, 62.0, 63.0, 64.0, 65.0, 67.0, 68.0, 69.0, 70.0]
        threshold = 70
        self.assertTrue(raisAlarm(valList, threshold))
        
    def test_raisAlarm_OK3(self):
        self.assertTrue(raisAlarm([77.0, 77.0, 77.0, 78.0, 81.0], 80))

    def test_raisAlarm_NOK1(self):
        valList = [70.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 70.0]
        threshold = 70
        self.assertFalse(raisAlarm(valList, threshold))

    def test_raisAlarm_NOK2(self):
        valList = [60.0, 60.0, 60.0, 62.0, 63.0, 64.0, 65.0, 67.0, 68.0, 70.0, 70.0]
        threshold = 70
        self.assertFalse(raisAlarm(valList, threshold))


    def test_clearAlarm_OK1(self):
        valList = [71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 70.0]
        threshold = 70
        self.assertTrue(clearAlarm(valList, threshold))

    def test_clearAlarm_OK2(self):
        valList = [80.0, 79.0, 78.0, 77.0, 76.0, 75.0, 74.0, 73.0, 72.0, 71.0, 70.0]
        threshold = 70
        self.assertTrue(clearAlarm(valList, threshold))

    def test_clearAlarm_NOK1(self):
        valList = [70.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 70.0]
        threshold = 70
        self.assertFalse(clearAlarm(valList, threshold))

    def test_clearAlarm_NOK2(self):
        valList = [79.0, 78.0, 77.0, 76.0, 75.0, 74.0, 73.0, 72.0, 71.0, 70.0, 70.0]
        threshold = 70
        self.assertFalse(clearAlarm(valList, threshold))


    def test_calculateThreshold_trendRising_65(self):
        self.assertEqual(calculateThreshold([65,65,65], True), 70)

    def test_calculateThreshold_trendRising_75(self):
        self.assertEqual(calculateThreshold([75,75,75], True), 80)

    def test_calculateThreshold_trendRising_85(self):
        self.assertEqual(calculateThreshold([85,85,85], True), 90)

    def test_calculateThreshold_trendRising_95(self):
        self.assertEqual(calculateThreshold([95,95,95], True), 100)

    def test_calculateThreshold_trendRising_all(self):
        self.assertEqual(calculateThreshold([69,69,69], True), 70)
        self.assertEqual(calculateThreshold([69,69,70], True), 70)
        self.assertEqual(calculateThreshold([69,70,71], True), 70)
        self.assertEqual(calculateThreshold([70,71,70], True), 80)

        self.assertEqual(calculateThreshold([79,79,79], True), 80)
        self.assertEqual(calculateThreshold([79,80,81], True), 80)
        self.assertEqual(calculateThreshold([80,81,80], True), 90)


    def test_calculateThreshold_trendFalling_70(self):
        self.assertEqual(calculateThreshold([70,70,70], False), 65)

    def test_calculateThreshold_trendFalling_80(self):
        self.assertEqual(calculateThreshold([80,80,80], False), 75)

    def test_calculateThreshold_trendFalling_90(self):
        self.assertEqual(calculateThreshold([90,90,90], False), 85)

    def test_calculateThreshold_trendFalling_100(self):
        self.assertEqual(calculateThreshold([100,100,100], False), 95)

    def test_calculateThreshold_trendFalling_all(self):
        self.assertEqual(calculateThreshold([80,79,78], False), 75)
        self.assertEqual(calculateThreshold([79,77,76], False), 75)
        self.assertEqual(calculateThreshold([77,76,75], False), 75)
        self.assertEqual(calculateThreshold([76,75,74], False), 75)
        self.assertEqual(calculateThreshold([75,74,73], False), 65)
        self.assertEqual(calculateThreshold([74,73,72], False), 65)
        self.assertEqual(calculateThreshold([73,72,71], False), 65)
        
        self.assertEqual(calculateThreshold([86,86,85], False), 85)
        self.assertEqual(calculateThreshold([85,85,85], False), 85)
        self.assertEqual(calculateThreshold([85,84,84], False), 75)

    def test_calculateThreshold_trend_edge(self):
        self.assertEqual(calculateThreshold([50,50], True), 70)
        self.assertEqual(calculateThreshold([50,50], False), 65)

        self.assertEqual(calculateThreshold([500,500], True), 170)
        self.assertEqual(calculateThreshold([500,500], False), 165)
    
    def test_extractLevels_ok(self):
        pos = 2
        tailOutput = "03.01.2026;05:00:01;58\n03.01.2026;05:01:01;58\n03.01.2026;05:02:02;58\n03.01.2026;05:03:01;58\n03.01.2026;05:04:02;59\n03.01.2026;05:05:01;59\n03.01.2026;05:06:01;58"
        levels = extractLevels(tailOutput, pos)
        self.assertEqual(levels, ['58','58','58','58','59','59','58'])
        
    def test_extractLevels_nok(self):
        pos = 2
        tailOutput = "03.01.2026;05:00:01;\n03.01.2026;05:01:01;58\n\n03.01.2026;05:03:01;58\n03.01.2026;;59\n03.01.2026;05:05:01;59\n;05:06:01;58"
        levels = extractLevels(tailOutput, pos)
        self.assertEqual(levels, ['','58','58','59','59','58'])
        
 
    def test_toNumbers(self):
         self.assertEqual(toNumbers(['58','58','58','58','59','59','58']), [58.0,58.0,58.0,58.0,59.0,59.0,58.0])
         self.assertEqual(toNumbers(['a','58',58,'58','dwe','59','-58']), [58.0,58.0,58.0,59.0,-58.0])

    
    def test_StoreAndGetThresholdAndTail(self):
        filenameStoreThreshold = "/tmp/test_WaterlevelThreshold.txt"
        threshold = 80
        
        #setup
        try: 
            os.remove(filenameStoreThreshold)
        except FileNotFoundError:
            pass
        
        #check tail no file present
        self.assertEqual(tail(filenameStoreThreshold), '')
        
        storeThreshold(filenameStoreThreshold, threshold)
        
        #check tail file present
        self.assertEqual(tail(filenameStoreThreshold), str(threshold))
        
        self.assertEqual(getStoredThreshold(filenameStoreThreshold), threshold)
        
        #cleanup
        try: 
            os.remove(filenameStoreThreshold)
        except FileNotFoundError:
            pass


    def test_roundUpOrDown(self):
        self.assertEqual(roundUpOrDown(55.5, 50.0), 55.0)
        self.assertEqual(roundUpOrDown(55.5, 60.0), 56.0)
        self.assertEqual(roundUpOrDown(55.0, 60.0), 55.0)
        self.assertEqual(roundUpOrDown(55.0, 50.0), 55.0)
        self.assertEqual(roundUpOrDown(55.1, 55.1), 55.1)

    def test_filterJumpsBigger10(self):
        self.assertEqual(filterJumpsBigger10([68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0]), [68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0])
        self.assertEqual(filterJumpsBigger10([60.0, 65.0, 70.0, 65.0, 60.0, 65.0, 70.0, 65.0]), [60.0, 65.0, 70.0, 65.0, 60.0, 65.0, 70.0, 65.0])
        self.assertEqual(filterJumpsBigger10([60.0, 61.0, 62.0, 80.0, 61.0, 62.0, 63.0, 60.0]), [60.0, 61.0, 62.0, 64.0, 61.0, 62.0, 63.0, 60.0])
        self.assertEqual(filterJumpsBigger10([60.0, 61.0, 62.0, 40.0, 61.0, 62.0, 63.0, 60.0]), [60.0, 61.0, 62.0, 58.0, 61.0, 62.0, 63.0, 60.0])
        self.assertEqual(filterJumpsBigger10([60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 63.0, 80.0]), [60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 63.0, 63.0])
        self.assertEqual(filterJumpsBigger10([60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 63.0, 40.0]), [60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 63.0, 59.0])
        self.assertEqual(filterJumpsBigger10([60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 78.0, 80.0]), [60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 66.0, 80.0])
        self.assertEqual(filterJumpsBigger10([60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 45.0, 40.0]), [60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 56.0, 40.0])
        self.assertEqual(filterJumpsBigger10([60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 60.0, 80.0]), [60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 60.0, 63.0])
        self.assertEqual(filterJumpsBigger10([60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 60.0, 45.0]), [60.0, 61.0, 62.0, 60.0, 61.0, 62.0, 60.0, 59.0])


#    def test_upper(self):
#        self.assertEqual('foo'.upper(), 'FOO')

#    def test_isupper(self):
#        self.assertTrue('FOO'.isupper())
#        self.assertFalse('Foo'.isupper())

#    def test_split(self):
#        s = 'hello world'
#        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
#        with self.assertRaises(TypeError):
#            s.split(2)


if __name__ == '__main__':
    unittest.main()
