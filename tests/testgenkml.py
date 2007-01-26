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


def suite():
  suite = unittest.TestSuite()
  suite.addTest(RegionNetworkLinkTestCase())
  suite.addTest(DefaultRegionTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

