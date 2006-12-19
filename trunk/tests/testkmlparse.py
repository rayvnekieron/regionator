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

import xml.dom.minidom
import kml.kmlparse
import kml.genxml


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


link_xml = ['<Link>\n',
            '<href>foo.kml</href>\n',
            '<viewRefreshMode>onRegion</viewRefreshMode>\n',
            '</Link>\n']

class ParseLinkTestCase(unittest.TestCase):
  def runTest(self):
    link_node = xml.dom.minidom.parseString("".join(link_xml))
    link = kml.kmlparse.ParseLink(link_node)
    assert link.href == 'foo.kml', 'Link href bad'
    assert link.viewRefreshMode == 'onRegion', 'Link viewRefreshMode bad'


llb_xml = ['<LatLonBox>\n',
            '<north>123</north>\n',
            '<south>-12.0987</south>\n',
            '<east>-52</east>\n',
            '<west>-80</west>\n',
            '</LatLonBox>\n']

class ParseLatLonBoxTestCase(unittest.TestCase):
  def runTest(self):
    llb_node = xml.dom.minidom.parseString("".join(llb_xml))
    llb = kml.kmlparse.ParseLatLonBox(llb_node)
    assert llb.north == '123', 'GetNSEW north bad'
    assert llb.south == '-12.0987', 'GetNSEW south bad'
    assert llb.east == '-52', 'GetNSEW east bad'
    assert llb.west == '-80', 'GetNSEW west bad'


region_xml = ['<Region>\n',
              '<LatLonAltBox>\n',
               '<north>56.65</north>\n',
               '<south>-78.7</south>\n',
               '<east>20.222</east>\n',
               '<west>1.56780</west>\n',
               '</LatLonAltBox>\n',
               '<Lod>\n',
               '<minLodPixels>128</minLodPixels>\n',
               '<maxLodPixels>1024</maxLodPixels>\n',
               '</Lod>\n',
               '</Region>\n']

class ParseRegionTestCase(unittest.TestCase):
  def runTest(self):
    # doc = xml.dom.minidom.parseString("".join(region_xml))
    kp = kml.kmlparse.KMLParse(None)
    kp.ParseString("".join(region_xml))
    (llab_node,lod_node) = kml.kmlparse.ParseRegion(kp.Doc())
    llab = kml.kmlparse.ParseLatLonAltBox(llab_node)
    lod = kml.kmlparse.ParseLod(lod_node)
    assert llab.north == '56.65', 'Region LatLonAltBox north bad'
    assert llab.south == '-78.7', 'Region LatLonAltBox south bad'
    assert llab.east == '20.222', 'Region LatLonAltBox east bad'
    assert llab.west == '1.56780', 'Region LatLonAltBox west bad'
    assert lod.minLodPixels == '128', 'Region Lod minLodPixels bad'
    assert lod.maxLodPixels == '1024', 'Region Lod maxLodPixels bad'


class HttpKmlTestCase(unittest.TestCase):
  def runTest(self):
    kp = kml.kmlparse.KMLParse('http://localhost/kml/foo.kml')
    doc = kp.Doc()
    namelist = doc.getElementsByTagName('name')
    assert namelist, 'http kml: no name element found'
    name = namelist[0]
    assert kml.kmlparse.GetText(namelist[0]) == 'foo name', 'bad name'


class HttpKmzTestCase(unittest.TestCase):
  def runTest(self):
    kp = kml.kmlparse.KMLParse('http://localhost/kml/foo.kmz')
    doc = kp.Doc()
    assert doc, 'http kmz: dom parse failed'
    namelist = doc.getElementsByTagName('name')
    assert namelist, 'http kmz: no name element found'
    name = namelist[0]
    assert kml.kmlparse.GetText(namelist[0]) == 'foo name', 'bad name'


class NoSuchFileTestCase(unittest.TestCase):
  def runTest(self):
   kp = kml.kmlparse.KMLParse('non-existent-file.kml')
   doc = kp.Doc()
   assert doc == None, 'failed to detect non-existent file'


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
  suite.addTest(ParseLinkTestCase())
  suite.addTest(ParseLatLonBoxTestCase())
  suite.addTest(ParseRegionTestCase())
  suite.addTest(HttpKmlTestCase())
  suite.addTest(HttpKmzTestCase())
  suite.addTest(NoSuchFileTestCase())
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())
