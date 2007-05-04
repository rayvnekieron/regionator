#!/usr/bin/python

"""
Copyright (C) 2007 Google Inc.

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

import os
import tempfile
import unittest
import xml.dom.minidom
import kml.checkregions
import kml.featureset
import kml.genkml
import kml.kmlparse
import kml.csvregionator

class SimpleFeatureSetTestCase(unittest.TestCase):
  def setUp(self):
    self.featureset = kml.featureset.FeatureSet()
    kp = kml.kmlparse.KMLParse('placemarks.kml')
    for placemark_node in kp.Doc().getElementsByTagName('Placemark'):
      self.featureset.AddFeature(placemark_node)
  def testSize(self):
    assert 136 == self.featureset.Size()
  def testNSEW(self):
    (n,s,e,w) = self.featureset.NSEW()
    assert n == 47.7572
    assert s == 46.2488
    assert e == 9.57312
    assert w ==  6.23596
  def testSplitThisRegion(self):
    want_size = self.featureset.Size()
    (n,s,e,w) = self.featureset.NSEW()
    region = kml.region.Region(n, s, e, w, '0')
    fs = self.featureset.SplitByRegion(region)
    assert want_size == fs.Size()
    assert 0 == self.featureset.Size()
    (got_n, got_s, got_e, got_w) = fs.NSEW()
    assert n == got_n
    assert s == got_s
    assert e == got_e
    assert w == got_w
  def testSplitSubRegion(self):
    total_size = self.featureset.Size()
    region = kml.region.Region(46.9, 46.4, 8.2, 7.1, '0')
    fs = self.featureset.SplitByRegion(region)
    assert total_size == fs.Size() + self.featureset.Size()
    (n,s,e,w) = fs.NSEW()
    assert n == 46.8959
    assert s == 46.4775
    assert e == 8.19533
    assert w == 7.17183
  def testSplitSome(self):
    orig_size = self.featureset.Size()
    half = orig_size/2
    (n,s,e,w) = self.featureset.NSEW()
    region = kml.region.Region(n, s, e, w, '0')
    fs = self.featureset.SplitByRegion(region, half)
    assert half == fs.Size()
    assert orig_size == self.featureset.Size() + fs.Size()
  def testCopyRegion(self):
    orig_size = self.featureset.Size()
    region = kml.region.Region(46.9, 46.4, 8.2, 7.1, '0')
    fs = self.featureset.CopyByRegion(region)
    assert orig_size == self.featureset.Size()
    (n,s,e,w) = fs.NSEW()
    assert n == 46.8959
    assert s == 46.4775
    assert e == 8.19533
    assert w == 7.17183

def PointPlacemark(id, lon, lat):
  pp = []
  pp.append('<Placemark id="%s">' % id)
  pp.append('<Point><coordinates>%f,%f</coordinates></Point>' % (lon,lat))
  pp.append('</Placemark>')
  return "".join(pp)

def CreatePointFeatureSet():
  a_node = xml.dom.minidom.parseString(PointPlacemark('a',1,1))
  b_node = xml.dom.minidom.parseString(PointPlacemark('b',-21,1))
  c_node = xml.dom.minidom.parseString(PointPlacemark('c',-21,-41))
  featureset = kml.featureset.FeatureSet()
  featureset.AddWeightedFeatureAtLocation(100, 1, 1, a_node)
  featureset.AddWeightedFeatureAtLocation(12345, -21, 1, b_node)
  featureset.AddWeightedFeatureAtLocation(5422, -21, -41, c_node)
  return featureset

class IndexFeatureSetTestCase(unittest.TestCase):
  def setUp(self):
    self.featureset = CreatePointFeatureSet()
  def testSize(self):
    assert 3 == self.featureset.Size()
  def testIterate(self):
    count = self.featureset.Size()
    i = 0
    while i < count:
      node = self.featureset.GetFeature(i)
      i += 1
  def testLoc(self):
    assert self.featureset.GetLoc(0) == (1,1)
    assert self.featureset.GetLoc(1) == (-21,1)
    assert self.featureset.GetLoc(2) == (-21,-41)

class SortFeatureSetTestCase(unittest.TestCase):
  def runTest(self):
    fs = CreatePointFeatureSet()
    fs.Sort()
    assert (-21,1) == fs.GetLoc(0)
    assert (-21,-41) == fs.GetLoc(1)
    assert (1,1) == fs.GetLoc(2)

class IterateFeatureSetTestCase(unittest.TestCase):
  def runTest(self):
    fs = CreatePointFeatureSet()
    fs.Sort()
    id_list = []
    for (w,lon,lat,feature) in fs:
      placemark_node = kml.kmlparse.GetFirstChildElement(feature, 'Placemark')
      id_list.append(placemark_node.getAttribute('id'))
    assert id_list[0] == 'b'
    assert id_list[1] == 'c'
    assert id_list[2] == 'a'

def LineStringPlacemark(id, n, s, e, w):
  ls = []
  ls.append('<Placemark id="%s">' % id)
  ls.append(kml.genkml.LineStringBox(n,s,e,w))
  ls.append('</Placemark>')
  return "".join(ls)

def CreateLineStringFeatureSet():
  a_node = xml.dom.minidom.parseString(LineStringPlacemark('a',1,0,1,0))
  b_node = xml.dom.minidom.parseString(LineStringPlacemark('b',2,0,2,0))
  c_node = xml.dom.minidom.parseString(LineStringPlacemark('c',3,-3,3,-3))
  featureset = kml.featureset.FeatureSet()
  featureset.AddLineString(a_node)
  featureset.AddLineString(b_node)
  featureset.AddLineString(c_node)
  return featureset

class LineStringFeatureSetTestCase(unittest.TestCase):
  def setUp(self):
    self.fs = CreateLineStringFeatureSet()
  def testLoc(self):
    assert (0,0) == self.fs.GetLoc(2)
    assert (1,1) == self.fs.GetLoc(1)
    assert (.5,.5) == self.fs.GetLoc(0)
  def testSort(self):
    self.fs.Sort()
    id_list = []
    for (w,lon,lat,feature) in self.fs:
      placemark_node = kml.kmlparse.GetFirstChildElement(feature, 'Placemark')
      id_list.append(placemark_node.getAttribute('id'))
    assert id_list[0] == 'c'
    assert id_list[1] == 'b'
    assert id_list[2] == 'a'

class FeatureSetRegionatorTestCase(unittest.TestCase):
  def setUp(self):
    fs = kml.csvregionator.CreateFeatureSet('gec.csv', None, 'latin_1')
    minlod = 128
    maxper = 4
    fs_handler = kml.featureset.FeatureSetRegionHandler(fs, minlod, maxper)
    rtor = kml.regionator.Regionator()
    rtor.SetRegionHandler(fs_handler)
    self.tmpdir = tempfile.mkdtemp()
    rtor.SetOutputDir(self.tmpdir)
    (n,s,e,w) = fs.NSEW()
    region = kml.region.RootSnap(n,s,e,w)
    rtor.SetVerbose(False)
    rtor.Regionate(region)

  def tearDown(self):
    for file in os.listdir(self.tmpdir):
      os.unlink(os.path.join(self.tmpdir, file))
    os.rmdir(self.tmpdir)

  def testKmlHierarchy(self):
    kml1 = os.path.join(self.tmpdir, '1.kml')
    region_handler = kml.checkregions.CheckRegions('-rk', kml1)
    (regions, files, errors) = region_handler.Statistics()
    assert 1422 == regions
    assert 356 == files
    assert 0 == errors


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleFeatureSetTestCase("testSize"))
  suite.addTest(SimpleFeatureSetTestCase("testNSEW"))
  suite.addTest(SimpleFeatureSetTestCase("testSplitThisRegion"))
  suite.addTest(SimpleFeatureSetTestCase("testSplitSubRegion"))
  suite.addTest(SimpleFeatureSetTestCase("testSplitSome"))
  suite.addTest(SimpleFeatureSetTestCase("testCopyRegion"))
  suite.addTest(IndexFeatureSetTestCase("testSize"))
  suite.addTest(IndexFeatureSetTestCase("testIterate"))
  suite.addTest(IndexFeatureSetTestCase("testLoc"))
  suite.addTest(SortFeatureSetTestCase())
  suite.addTest(IterateFeatureSetTestCase())
  suite.addTest(LineStringFeatureSetTestCase("testLoc"))
  suite.addTest(LineStringFeatureSetTestCase("testSort"))
  suite.addTest(FeatureSetRegionatorTestCase("testKmlHierarchy"))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

