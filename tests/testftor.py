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
import os
import tempfile
import kml.featureregionator


class NullFeatureRegionatorTestCase(unittest.TestCase):
  def runTest(self):
    # Direct use of kml.featureregionator.FeatureRegionator() does nothing
    ftor = kml.featureregionator.FeatureRegionator()
    ftor.SetVerbose(False)
    dir = tempfile.mktemp()
    ret = ftor.Regionate('placemarks.kml', 128, 16, 'none.kml', dir)
    assert ret == None
    assert os.access('none.kml', os.F_OK) == 0
    # Verify a directory was created
    assert os.access(dir, os.F_OK) != 0
    os.rmdir(dir)
    # Essentially asserts the directory was empty
    assert os.access(dir, os.F_OK) == 0


class PlacemarkRegionatorTestCase(unittest.TestCase):
  def setUp(self):
    class pmrtor(kml.featureregionator.FeatureRegionator):
      def ExtractItems(self):
        doc = self.GetDoc()
        placemark_nodes = doc.getElementsByTagName('Placemark')
        for placemark in placemark_nodes:
          point_nodes = placemark.getElementsByTagName('Point')
          for point in point_nodes:
            coord_nodes = point.getElementsByTagName('coordinates')
            for coord in coord_nodes:
              lonlat = self.AddPointCoordinates(coord)
              if lonlat:
                item = (lonlat, coord.toxml())
                self.AddItem(item)

    self.__dir = tempfile.mktemp()
    self.__root = tempfile.mktemp()
    self.__pmr = pmrtor()
    self.__pmr.SetVerbose(False)

  def tearDown(self):
    os.unlink(self.__root)
    for file in os.listdir(self.__dir):
      os.unlink(os.path.join(self.__dir, file))
    os.rmdir(self.__dir)

  def testRegionate(self):
    self.__pmr.Regionate('placemarks.kml', 256, 16, self.__root, self.__dir)
    (n,s,e,w) = self.__pmr.NSEW()
    assert n == 47.7572
    assert s == 46.2488
    assert e == 9.57312
    assert w == 6.23596
    assert len(os.listdir(self.__dir)) == 14


class LineStringRegionatorTestCase(unittest.TestCase):
  def setUp(self):
    class lsrtor(kml.featureregionator.FeatureRegionator):
      def ExtractItems(self):
        doc = self.GetDoc()
        placemark_nodes = doc.getElementsByTagName('Placemark')
        for placemark in placemark_nodes:
          ls_nodes = placemark.getElementsByTagName('LineString')
          for ls in ls_nodes:
            coord_nodes = ls.getElementsByTagName('coordinates')
            for coord in coord_nodes:
              (size,lonlat) = self.AddLinestringCoordinates(coord)
              if lonlat:
                item = (size, lonlat, coord.toxml())
                self.AddWeightedItem(item)

    self.__dir = tempfile.mktemp()
    self.__root = tempfile.mktemp()
    self.__lsr = lsrtor()
    self.__lsr.SetVerbose(False)

  def tearDown(self):
    os.unlink(self.__root)
    for file in os.listdir(self.__dir):
      os.unlink(os.path.join(self.__dir, file))
    os.rmdir(self.__dir)

  def testRegionate(self):
    rtor = self.__lsr.Regionate('marin.kml', 256, 16, self.__root, self.__dir)
    assert len(rtor.QidList()) == 146, 'ftor ls qidlist bad'
    assert rtor.MaxDepth() == 9, 'ftor ls max depth bad'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(NullFeatureRegionatorTestCase())
  suite.addTest(PlacemarkRegionatorTestCase('testRegionate'))
  suite.addTest(LineStringRegionatorTestCase('testRegionate'))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

