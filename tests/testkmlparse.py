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
$URL: https://regionator.googlecode.com/svn/trunk/tests/testparse.py $
$Revision: 80 $
$Date: 2006-10-24 10:44:05 -0700 (Tue, 24 Oct 2006) $
"""

import unittest

import kml.kmlparse


class GroundOverlayParseTestCase(unittest.TestCase):
  def setUp(self):
    self.__kmldoc = kml.kmlparse.KMLParse('go.kml')
  def testLatLonBox(self):
    latlonbox = self.__kmldoc.ExtractLatLonBox()
    assert latlonbox.north == '20', 'LatLonBox north bad'
    assert latlonbox.south == '-20', 'LatLonBox south bad'
    assert latlonbox.east == '20', 'LatLonBox east bad'
    assert latlonbox.west == '-20', 'LatLonBox west bad'
  def testIcon(self):
    icon = self.__kmldoc.ExtractIcon()
    assert icon.href == 'foo.jpg', 'Icon href bad'
  def testTimeSpan(self):
    timespan = self.__kmldoc.ExtractTimeSpan()
    assert timespan.begin == '2006', 'TimeSpan begin bad'
    assert timespan.end == '2007', 'TimeSpan end bad'
  def testGroundOverlay(self):
    go = self.__kmldoc.ExtractGroundOverlay()
    assert go.drawOrder == '10', 'drawOrder bad'


class KMZParseTestCase(unittest.TestCase):
  def setUp(self):
    self.__kmldoc = kml.kmlparse.KMLParse('coit.kmz')
  def testLocation(self):
    location = self.__kmldoc.ExtractLocation()
    assert location.longitude == '-122.405843291645', 'KMZ Location bad'
  def testLookAt(self):
    lookat = self.__kmldoc.ExtractLookAt()
    assert lookat.tilt == '49.82584784628866', 'KMZ LookAt bad'


class RegionParseTestCase(unittest.TestCase):
  def setUp(self):
    self.__kmldoc = kml.kmlparse.KMLParse('region.kml')
  def testLatLonAltBox(self):
    llab = self.__kmldoc.ExtractLatLonAltBox()
    assert llab.west == '-80.859375', 'LatLonAltBox west bad'
    assert llab.minAltitude == '100000', 'LatLonAltBox minAltitude bad'
    assert llab.maxAltitude == '100001', 'LatLonAltBox maxAltitude bad'
    assert llab.altitudeMode == 'absolute', 'LatLonAltBox altidueMode bad'


class NoSuchElementTestCase(unittest.TestCase):
  def setUp(self):
    self.__kmldoc = kml.kmlparse.KMLParse('ksc-llb-0.kml')
  def testLatLonAltBox(self):
    latlonaltbox = self.__kmldoc.ExtractLatLonAltBox()
    assert not latlonaltbox, 'LatLonAltbox not expected'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(GroundOverlayParseTestCase("testLatLonBox"))
  suite.addTest(GroundOverlayParseTestCase("testIcon"))
  suite.addTest(GroundOverlayParseTestCase("testTimeSpan"))
  suite.addTest(GroundOverlayParseTestCase("testGroundOverlay"))
  suite.addTest(KMZParseTestCase("testLocation"))
  suite.addTest(KMZParseTestCase("testLookAt"))
  suite.addTest(RegionParseTestCase("testLatLonAltBox"))
  suite.addTest(NoSuchElementTestCase("testLatLonAltBox"))
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())
