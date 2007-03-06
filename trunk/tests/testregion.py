#!/usr/bin/python

"""
Copyright (C) 2006 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
$URL$
$Revision$
$Date$
"""

import unittest


# Test of some Region methods.

import kml.region
import kml.genkml
import kml.genxml


class SimpleRegionTestCase(unittest.TestCase):
  def setUp(self):
    self.r = kml.region.Region(20,10,40,20,'0')
  def testQid(self):
    assert self.r.Qid() == '0', 'Qid bad'
  def testDepth(self):
    assert self.r.Depth() == 1, 'Depth bad'
  def testChildren(self):
    for q in ['0','1','2','3']:
      rc = self.r.Child(q)
      qid = '0' + q
      assert rc.Qid() == qid, 'child Qid bad'
      assert rc.Depth() == 2, 'child Depth bad'


class SubRegionTestCase(unittest.TestCase):
  def runTest(self):
    region = kml.region.Region(30,10,40,20,'0')
    region000 = region.Region('000')
    region033 = region.Region('033')
    assert region000.NSEW() == (30,25,25,20), 'subregion 000 bad'
    assert region033.NSEW() == (15,10,40,35), 'subregion 033 bad'


def CreateAncestors(kmlfile):
  root = kml.region.RootRegion()
  n = 21.2
  s = 19.5
  e = -115.4
  w = -117.5
  r = root.Snap(n,s,e,w)
  (_n,_s,_e,_w) = r.NSEW()
  print 'orig',n,s,e,w
  print r.Qid(),_n,_s,_e,_w

  document = kml.genxml.Document()
  node = r.Qid()
  d = 1
  while d <= r.Depth():
    qid = node[0:d]
    _r = root.Region(qid)
    (_n,_s,_e,_w) = _r.NSEW()
    document.Add_Feature(kml.genkml.LatLonOutline(_n,_s,_e,_w,qid))
    d += 1
  
  document.Add_Feature(kml.genkml.LatLonOutline(n,s,e,w,'orig'))

  k = kml.genxml.Kml()
  k.Feature = document.xml()
  
  f = open(kmlfile,'w')
  f.write(k.xml())
  f.close


class RegionLocationTestCase(unittest.TestCase):
  def runTest(self):
    nw = kml.region.Location('0')
    ne = kml.region.Location('1')
    sw = kml.region.Location('2')
    se = kml.region.Location('3')
    assert nw == (0,1), 'nw bad'
    assert ne == (1,1), 'ne bad'
    assert sw == (0,0), 'sw bad'
    assert se == (1,0), 'se bad'

n00 = kml.region.Grid('00')
n01 = kml.region.Grid('01')
n02 = kml.region.Grid('02')
n03 = kml.region.Grid('03')
n000 = kml.region.Grid('000')


class RegionGridTestCase(unittest.TestCase):
  def runTest(self):
    n03 = kml.region.Grid('03')
    n033 = kml.region.Grid('033')
    n0333 = kml.region.Grid('0333')
    assert n03 == (1,0), '03 bad'
    assert n033 == (3,0), '033 bad'
    assert n0333 == (7,0), '0333 bad'


class SnapPointTestCase(unittest.TestCase):
  def runTest(self):
    root = kml.region.RootRegion()
    lon = -122.082163
    lat =   37.420422
    depth = 18
    ra = root.SnapPoint(lon, lat, depth)
    rb = kml.region.RootSnapPoint(lon, lat, depth)
    (n,s,e,w) = ra.NSEW()
    assert n == 37.42218017578125, 'north bad'
    assert s == 37.41943359375, 'sourth bad'
    assert e == -122.080078125, 'east bad'
    assert w == -122.08282470703125, 'west bad'
    assert ra.NSEW() == rb.NSEW(), 'bad NSEW'
    assert ra.Depth() == depth, 'bad depth'

class ParentTestCase(unittest.TestCase):
  def setUp(self):
    self.__root = kml.region.RootRegion()
  def testRoot(self):
    assert self.__root.ParentQid() == '0', 'Bad root parent'
  def testDeeper(self):
    region = self.__root.Region('01230321')
    assert region.ParentQid() == '0123032', 'Bad deeper region parent'


class WhichChildTestCase(unittest.TestCase):
  def runTest(self):
    root = kml.region.RootRegion()
    nw = root.WhichChildForPoint(-10, 10)
    ne = root.WhichChildForPoint(10, 10)
    se = root.WhichChildForPoint(10, -10)
    sw = root.WhichChildForPoint(-10, -10)
    assert nw.Qid() == '00'
    assert ne.Qid() == '01'
    assert sw.Qid() == '02'
    assert se.Qid() == '03'
 

def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleRegionTestCase("testQid"))
  suite.addTest(SimpleRegionTestCase("testDepth"))
  suite.addTest(SimpleRegionTestCase("testChildren"))
  suite.addTest(SubRegionTestCase())
  suite.addTest(RegionLocationTestCase())
  suite.addTest(RegionGridTestCase())
  suite.addTest(SnapPointTestCase())
  suite.addTest(ParentTestCase("testRoot"))
  suite.addTest(ParentTestCase("testDeeper"))
  suite.addTest(WhichChildTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

CreateAncestors('ancestors.kml')
