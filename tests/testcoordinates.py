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
    

# Tests for the Coord3d and Coord3dArray classes:

class BasicCoord3dTestCase(unittest.TestCase):
  def runTest(self):

    # Default initialization.
    c3d = kml.coordinates.Coord3d()
    assert 0.0 == c3d.lon == c3d.lat == c3d.alt

    # Initialization from string.
    s = '-1, 2'
    c3d.from_string(s)
    assert (-1.0, 2.0) == (c3d.lon, c3d.lat)
    s = '-1, 2, 100'
    c3d.from_string(s)
    assert (-1.0, 2.0, 100.0) == (c3d.lon, c3d.lat, c3d.alt)

    # Initialization from tuple.
    t = (-3, 4)
    c3d = kml.coordinates.Coord3d(t)
    assert (-3.0, 4.0) == (c3d.lon, c3d.lat)
    t = (-3, 4, 200)
    c3d = kml.coordinates.Coord3d(t)
    assert (-3.0, 4.0, 200) == (c3d.lon, c3d.lat, c3d.alt)

    # Initialization from list.
    l = [-5, 6]
    c3d = kml.coordinates.Coord3d(l)
    assert (-5.0, 6.0) == (c3d.lon, c3d.lat)
    l = [-5, 6, 300]
    c3d = kml.coordinates.Coord3d(l)
    assert (-5.0, 6.0, 300.0) == (c3d.lon, c3d.lat, c3d.alt)

    # Explicit setting of kml.coordinates
    c3d.lon,c3d.lat,c3d.alt = 1,2,3
    assert (1.0,2.0,3.0) == (c3d.lon,c3d.lat,c3d.alt)

    # String output.
    assert '1.000000,2.000000,3.000000' == c3d.to_string()


class BasicCoord3dArrayTestCase(unittest.TestCase):

  def testParse(self, coords, expected=None):

    """Helper function. The coords arg can be a string, tuple, list, list of
    lists, etc. We hand the content to kml.coordinates.Coord3darr() and ensure
    it is parsed correctly. If testing a string, theexpected arg is required
    and is a list of the expected lon,lat,alt coords.
    """
    c3darr = kml.coordinates.Coord3dArray(coords)
    parsed_coords = c3darr.coords
    if isinstance('', coords.__class__):
      assert expected is not None
      c0 = kml.coordinates.Coord3d(expected[0])
      c1 = kml.coordinates.Coord3d(expected[1])
      c2 = kml.coordinates.Coord3d(expected[2])
    else:
      c0 = kml.coordinates.Coord3d(coords[0])
      c1 = kml.coordinates.Coord3d(coords[1])
      c2 = kml.coordinates.Coord3d(coords[2])
    c = [c0, c1, c2]
    for i in range(3):
      assert c[i].lon == parsed_coords[i].lon
      assert c[i].lat == parsed_coords[i].lat
      assert c[i].alt == parsed_coords[i].alt

  def runTest(self):

    # Default initialization.
    c3darr = kml.coordinates.Coord3dArray()
    assert [] == c3darr.coords

    # Initialization from sloppy space-delimited string, first coordinate has
    # implied altitude of 0.
    s = '0,1 2, 3, 4 5 , 6,   7'
    self.testParse(s, ['0,1,0','2,3,4','5,6,7'])

    # Initialization from list of sloppy strings.
    l1 = ['2,4', '6, 8, 10', ' 12 , 14  ,   16']
    self.testParse(l1)

    # Initialization from list of lists.
    l2 = [[9,8,7], [6,5,4], [3,2]]
    self.testParse(l2)

    # Initialization from tuple of sloppy strings.
    t1 = ('3,5', '7, 9, 11', ' 13 , 15  ,   17')
    self.testParse(t1)

    # Initialization from tuple of tuples.
    t2 = ((3,1), (4,1,5), (9,2,6))
    self.testParse(t2)


class ClosedLoopTestCase(unittest.TestCase):

  def runTest(self):
    unclosed_square = [[0,0], [1,0], [1,1], [0,1]]
    c3darr = kml.coordinates.Coord3dArray(unclosed_square)
    assert False == c3darr.first_equals_last()
    c3darr.close_loop()
    assert True == c3darr.first_equals_last()
    coords = c3darr.coords
    assert 5 == len(coords)
    assert 0.0 == coords[4].lon == coords[4].lat == coords[4].alt


class WindingOrderTestCase(unittest.TestCase):

  def runTest(self):
    cw = [[0,0], [0,1], [1,1], [1,0], [0,0]]
    c3darr = kml.coordinates.Coord3dArray(cw)
    assert True == c3darr.first_equals_last()
    assert True == c3darr.is_clockwise()

    ccw = [[1,1,1],[2,1,1],[2,2,1]]
    c3darr = kml.coordinates.Coord3dArray(ccw)
    assert False == c3darr.is_clockwise()
    assert False == c3darr.first_equals_last()
    c3darr.close_loop()
    assert True == c3darr.first_equals_last()

    # straight line has ccw winding order...
    sl = [[0,0], [1,1], [2,2]]
    c3darr = kml.coordinates.Coord3dArray(sl)
    assert False == c3darr.is_clockwise()


def suite():
  suite = unittest.TestSuite()
  suite.addTest(JHTTestCase())
  suite.addTest(MarinTestCase())
  suite.addTest(NoAltTestCase())
  suite.addTest(SloppyPointTestCase())
  suite.addTest(BasicCoord3dTestCase())
  suite.addTest(BasicCoord3dArrayTestCase())
  suite.addTest(ClosedLoopTestCase())
  suite.addTest(WindingOrderTestCase())
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())
