#!/usr/bin/python

import unittest

import kml.coordinates

class JHTTestCase(unittest.TestCase):
  def runTest(self):
    jht = '-71.07513662574,42.349230901775,240.792015658496'
    jhtpoints = kml.coordinates.ParseCoordinates(jht)
    assert len(jhtpoints) == 1, 'result not single point'
    jhtpoint = jhtpoints[0]
    assert jhtpoint[0] == -71.07513662574, 'bad lon'
    assert jhtpoint[1] == 42.349230901775, 'bad lat'
    assert jhtpoint[2] == 240.792015658496, 'bad alt'


marin = '-122.585721893393,38.1858473049571,0 -122.585644410362,38.1857929553359,0 -122.585556503179,38.1856889999166,0 -122.585494823827,38.1854905060747,0 -122.585385202212,38.1853143734671,0 -122.585264467809,38.1852103014087,0 -122.585044689036,38.1850788402271,0 -122.584823355957,38.1849699043878,0 -122.584593027341,38.184811367369,0 -122.584502802818,38.1847389467015,0 -122.584411381412,38.1846259654161,0 -122.584304720609,38.18443181728831,0 -122.584269831524,38.1842919993342,0 -122.584289026067,38.1841794112014,0 -122.584327668054,38.1840353484151,0 -122.584327363798,38.1839632472476,0 -122.584281997697,38.1839090108928,0 -122.58421303028,38.1838637031055,0 -122.583908308494,38.183736443945,0 -122.583666388072,38.18360940762871,0 -122.583591737832,38.1835595729854,0 -122.583536103727,38.1834286934266,0 -122.583450215034,38.1833472748728,0 -122.583434317056,38.1833383323323,0 -122.5833050947,38.1832656451818,0 -122.583228838208,38.1832473483726,0 -122.583054125632,38.1832241942132,0 -122.582958098019,38.1832404481718,0 -122.582845538488,38.1832595002691,0 -122.582705280477,38.1833265936221,0 -122.582451856246,38.1834653828257,0 -122.582263989375,38.1834962555804,0 -122.582092156802,38.1834686040237,0 -122.582015238226,38.1834412915501,0 -122.581910160203,38.1833462845094,0 -122.581855596201,38.1832784955622,0 -122.581679677317,38.182966934687,0 -122.581626901582,38.1828360644473,0 -122.581503432652,38.1825877785307,0 -122.581317518198,38.1824023564811,0 -122.581100746556,38.182122192211,0'

class MarinTestCase(unittest.TestCase):
  def runTest(self):
    mpoints = kml.coordinates.ParseCoordinates(marin)
    assert len(mpoints) == 41, 'result not 41 points'
    mp0 = mpoints[0]
    assert mp0[0] == -122.585721893393, 'point0 bad lon'
    assert mp0[1] == 38.1858473049571, 'point0 bad lat'
    mp40 = mpoints[40]
    assert mp40[0] == -122.581100746556, 'point40 bad lon'
    assert mp40[1] == 38.182122192211, 'point40 bad lat'
    assert mp40[2] == 0, 'point40 bad alt'


class NoAltTestCase(unittest.TestCase):
  def runTest(self):
    mycoord = '21.456,78.123'
    parsed = kml.coordinates.ParseCoordinates(mycoord)
    assert len(parsed) == 1, 'result not 1 point'
    p0 = parsed[0]
    assert len(p0) == 2, 'result not simple pair'
    assert p0[0] == 21.456, 'bad lon'
    assert p0[1] == 78.123, 'bad lat'


class SloppyPointTestCase(unittest.TestCase):
  def runTest(self):
    sloppypoint = '6.31914, 46.6487,20' # note the space
    parsed = kml.coordinates.ParseCoordinates(sloppypoint)
    assert len(parsed) == 1, 'result not 1 point'
    p0 = parsed[0]
    assert p0[0] == 6.31914, 'bad lon'
    assert p0[1] == 46.6487, 'bad lat'
    assert p0[2] == 20, 'bad alt'
    

def suite():
  suite = unittest.TestSuite()
  suite.addTest(JHTTestCase())
  suite.addTest(MarinTestCase())
  suite.addTest(NoAltTestCase())
  suite.addTest(SloppyPointTestCase())
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())
