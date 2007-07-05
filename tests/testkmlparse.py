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
    (llab,lod) = kml.kmlparse.ParseRegion(kp.Doc())
    assert llab.north == '56.65', 'Region LatLonAltBox north bad'
    assert llab.south == '-78.7', 'Region LatLonAltBox south bad'
    assert llab.east == '20.222', 'Region LatLonAltBox east bad'
    assert llab.west == '1.56780', 'Region LatLonAltBox west bad'
    assert lod.minLodPixels == '128', 'Region Lod minLodPixels bad'
    assert lod.maxLodPixels == '1024', 'Region Lod maxLodPixels bad'


class HttpKmlTestCase(unittest.TestCase):
  def runTest(self):
    kp = kml.kmlparse.KMLParse('http://regionator.googlecode.com/files/foo.kml')
    doc = kp.Doc()
    assert doc, 'http kml: fetch or parse failed'
    namelist = doc.getElementsByTagName('name')
    assert namelist, 'http kml: no name element found'
    name = namelist[0]
    assert kml.kmlparse.GetText(namelist[0]) == 'foo name', 'bad name'


class HttpKmzTestCase(unittest.TestCase):
  def runTest(self):
    kp = kml.kmlparse.KMLParse('http://regionator.googlecode.com/files/foo.kmz')
    doc = kp.Doc()
    assert doc, 'http kmz: dom parse failed'
    namelist = doc.getElementsByTagName('name')
    assert namelist, 'http kmz: no name element found'
    name = namelist[0]
    assert kml.kmlparse.GetText(namelist[0]) == 'foo name', 'bad name'

# XXX http://regionator.googlecode.com/files/foo.kmz/foo.kml


class NoSuchFileTestCase(unittest.TestCase):
  def runTest(self):
   kp = kml.kmlparse.KMLParse('non-existent-file.kml')
   doc = kp.Doc()
   assert doc == None, 'failed to detect non-existent file'


class RegionExtractTestCase(unittest.TestCase):
  def runTest(self):
    kp = kml.kmlparse.KMLParse(None)
    kp.ParseString("".join(region_xml))
    assert kp.Doc()
    (llab, lod) = kp.ExtractRegion()
    assert llab
    assert llab.north == '56.65', 'RegionExtract LatLonAltBox north bad'
    assert llab.south == '-78.7', 'RegionExtract LatLonAltBox south bad'
    assert llab.east == '20.222', 'RegionExtract LatLonAltBox east bad'
    assert llab.west == '1.56780', 'RegionExtract LatLonAltBox west bad'
    assert lod
    assert lod.minLodPixels == '128', 'RegionExtract Lod minLodPixels bad'
    assert lod.maxLodPixels == '1024', 'RegionExtract Lod maxLodPixels bad'


class GetFirstChildElementNoNodeTestCase(unittest.TestCase):
  def runTest(self):
    ret = kml.kmlparse.GetFirstChildElement(None, 'foo')
    assert ret == None, 'GetFirstChildElement failed on null doc'


class GetFirstChildElementSimpleTestCase(unittest.TestCase):
  def runTest(self):
    doc = xml.dom.minidom.parseString("".join(region_xml))
    region_node = kml.kmlparse.GetFirstChildElement(doc, 'Region')
    assert region_node, 'GetFirstChildElement failed to find Region'
    assert region_node.tagName == 'Region', 'GetFirstChildElement bad tag'

class NoneNodeTestCase(unittest.TestCase):
  def runTest(self):
    assert None == kml.kmlparse.GetText(None)
    assert None == kml.kmlparse.GetCDATA(None)
    assert None == kml.kmlparse.GetSimpleElementText(None, 'ignored')
    assert None == kml.kmlparse.GetFirstChildElement(None, 'ignored')

class ParseFeatureRegionTestCase(unittest.TestCase):
  def runTest(self):
    doc = xml.dom.minidom.parse('rbnl.kml')
    node = kml.kmlparse.GetFirstChildElement(doc, 'NetworkLink')
    (llab,lod) = kml.kmlparse.ParseFeatureRegion(node)
    assert '-28.828125' == llab.north
    assert '-45.125' == llab.south
    assert '10.15625' == llab.east
    assert '-20.859375' == llab.west
    assert '122' == lod.minLodPixels

class GetNetworkLinkHrefTestCase(unittest.TestCase):
  def runTest(self):
    doc = xml.dom.minidom.parse('rbnl.kml')
    node = kml.kmlparse.GetFirstChildElement(doc, 'NetworkLink')
    href = kml.kmlparse.GetNetworkLinkHref(node)
    assert 'non-existent-file.kml' == href

    doc = xml.dom.minidom.parse('hrefcdata.kml')
    node = kml.kmlparse.GetFirstChildElement(doc, 'NetworkLink')
    href = kml.kmlparse.GetNetworkLinkHref(node)
    assert 'http://z2.abc.com/a2e/goo.kml' == href


class ParseUsingCodecTestCase(unittest.TestCase):
  def runTest(self):
    (xml_header, xml_data) = kml.kmlparse.SplitXmlHeaderFromFile('es-utf8.kml')
    assert 'utf_8' == kml.kmlparse.GetEncoding(xml_header)
    # Parser fails due to wrong encoding
    kp = kml.kmlparse.KMLParse('es-utf8.kml')
    assert None == kp.Doc()
    # Parse with the proper codec for file contents:
    kp = kml.kmlparse.KMLParse(None)
    kp.ParseStringUsingCodec(xml_data, 'latin1')
    doc = kp.Doc()
    style = doc.getElementsByTagName('Style')
    # This file is known to have one Style element with the asserted id
    assert 1 == len(style)
    assert 'MyStyleId' == style[0].getAttribute('id')

point_2d_xml = ['<Placemark>',
                '<Point><coordinates>-123,38</coordinates></Point>',
                '</Placemark>']

point_3d_xml = ['<Placemark>',
                '<Point><coordinates>10.1,-34.8,10001</coordinates></Point>',
                '</Placemark>']

class ParsePointLocTestCase(unittest.TestCase):
  def runTest(self):
    node = xml.dom.minidom.parseString("".join(point_2d_xml))
    (lon,lat) = kml.kmlparse.ParsePointLoc(node)
    assert -123 == lon
    assert 38 == lat

    node = xml.dom.minidom.parseString("".join(point_3d_xml))
    (lon,lat,alt) = kml.kmlparse.ParsePointLoc(node)
    assert 10.1 == lon
    assert -34.8 == lat
    assert 10001 == alt

class StyleUrlTestCase(unittest.TestCase):
  def runTest(self):
    (url, id) = kml.kmlparse.ParseStyleUrlText('hi.kml#foo')
    assert url == 'hi.kml'
    assert id == 'foo'
    (url, id) = kml.kmlparse.ParseStyleUrlText('no-pound-sign-here')
    assert url == None
    assert id == None
    (url, id) = kml.kmlparse.ParseStyleUrlText('#id_only')
    assert url == None
    assert id == 'id_only'
    (url, id) = kml.kmlparse.ParseStyleUrlText('http://foo.com/goo.kml')
    assert url == None
    assert id == None


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
  suite.addTest(RegionExtractTestCase())
  suite.addTest(GetFirstChildElementNoNodeTestCase())
  suite.addTest(GetFirstChildElementSimpleTestCase())
  suite.addTest(NoneNodeTestCase())
  suite.addTest(ParseFeatureRegionTestCase())
  suite.addTest(GetNetworkLinkHrefTestCase())
  suite.addTest(ParseUsingCodecTestCase())
  suite.addTest(ParsePointLocTestCase())
  suite.addTest(StyleUrlTestCase())
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())
