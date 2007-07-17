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

import kml.genkml
import kml.kmlparse
import xml.dom.minidom


class DefaultRegionTestCase(unittest.TestCase):
  def runTest(self):
    n = 22.22
    s = -78.555
    e = -88.99
    w = -101.101
    region = kml.genkml.Region(n,s,e,w)
    kp = kml.kmlparse.KMLParse(None)
    kp.ParseString(region)
    llab = kp.ExtractLatLonAltBox()
    assert n == float(llab.north)
    assert s == float(llab.south)
    assert e == float(llab.east)
    assert w == float(llab.west)
    assert None == llab.minAltitude
    assert None == llab.maxAltitude

#class BasicRegionTestCase(unittest.TestCase):
#  def runTest(self):
#    Region(n,s,e,w,minalt=0,maxalt=0,minpx=128,minfade=0,maxpx=1024,maxfade=0)


class RegionNetworkLinkTestCase(unittest.TestCase):
  def runTest(self):
    n = 75.2
    s = -16.7
    e = 101.1
    w = -99.8
    name = 'name'
    href = 'there.kml'
    minpx = 123
    maxpx = 1234
    rnl = kml.genkml.RegionNetworkLink(n, s, e, w, name, href, minpx, maxpx)
    kp = kml.kmlparse.KMLParse(None)
    kp.ParseString(rnl)
    llab = kp.ExtractLatLonAltBox()
    assert n == float(llab.north)
    assert s == float(llab.south)
    assert e == float(llab.east)
    assert w == float(llab.west)
    link = kp.ExtractLink()
    assert link.href == href
    assert link.viewRefreshMode == 'onRegion'

linestring_kml = ['<LineString>',
                  '<tessellate>1</tessellate>',
                  '<coordinates>1.100000,-21.340000',
                  '-122.567000,38.123000</coordinates>',
                  '</LineString>']

class SimpleLineStringTestCase(unittest.TestCase):
  def runTest(self):
    a_lon = 1.1
    a_lat = -21.34
    b_lon = -122.567
    b_lat = 38.123
    ls_got = kml.genkml.SimpleLineString(a_lon, a_lat, b_lon, b_lat)
    ls_want = '\n'.join(linestring_kml) + '\n'
    assert ls_want == ls_got

class Test8601(unittest.TestCase):
  def runTest(self):
    assert '1970-01-01T00:00:00Z' ==  kml.genkml.CreateISO8601(0)
    assert '2007-06-12T20:17:36Z' ==  kml.genkml.CreateISO8601(1181679456)

class TestLookAt(unittest.TestCase):
  def runTest(self):
    lon = 123
    lat = 45
    range = 9876
    tilt = 42
    heading = 187
    lookat_kml = kml.genkml.LookAt(lon, lat, range, tilt, heading)
    lookat_node = xml.dom.minidom.parseString(lookat_kml)
    lookat = kml.kmlparse.ParseLookAt(lookat_node)
    assert lon == float(lookat.longitude)
    assert lat == float(lookat.latitude)
    assert range == float(lookat.range)
    assert tilt == float(lookat.tilt)
    assert heading == float(lookat.heading)

class TestCamera(unittest.TestCase):
  def runTest(self):
    lon = 123
    lat = 45
    alt = 10101
    heading = 187
    tilt = 42
    roll = -15.15
    altmode = 'absolute'
    camera_kml = kml.genkml.Camera(lon, lat, alt, heading, tilt, roll, altmode)
    camera_node = xml.dom.minidom.parseString(camera_kml)
    camera = kml.kmlparse.ParseCamera(camera_node)
    assert lon == float(camera.longitude)
    assert lat == float(camera.latitude)
    assert alt == float(camera.altitude)
    assert heading == float(camera.heading)
    assert tilt == float(camera.tilt)
    assert roll == float(camera.roll)
    assert altmode == camera.altitudeMode

def suite():
  suite = unittest.TestSuite()
  suite.addTest(RegionNetworkLinkTestCase())
  suite.addTest(DefaultRegionTestCase())
  suite.addTest(SimpleLineStringTestCase())
  suite.addTest(Test8601())
  suite.addTest(TestLookAt())
  suite.addTest(TestCamera())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

