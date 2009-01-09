#!/usr/bin/env python

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

import xml.dom.minidom
import kml.bbox
import kml.genkml

ls_kml = ['<LineString>',
          '<coordinates>123,45 122,44 121,46 124,48</coordinates>',
          '</LineString>']


class TestGetCoordinatesBBOX(unittest.TestCase):
  def runTest(self):
    ls_node = xml.dom.minidom.parseString(''.join(ls_kml))
    (n,s,e,w) = kml.bbox.GetCoordinatesBBOX(ls_node)
    assert 48 == n
    assert 44 == s
    assert 124 == e
    assert 121 == w


class TestGetPlacemarkBBOX(unittest.TestCase):
  def runTest(self):
    box_kml = kml.genkml.Box(67.7, -2, -67, -120.12, 'abox')
    pm_node = xml.dom.minidom.parseString(box_kml)
    (n,s,e,w) = kml.bbox.GetPlacemarkBBOX(pm_node)
    assert 67.7 == n
    assert -2 == s
    assert -67 == e
    assert -120.12 == w


class TestNoGeomPlacemarkBBOX(unittest.TestCase):
  def runTest(self):
    pm_nogeom_kml = '<Placemark><name>no geometry</name></Placemark>'
    pm_nogeom_node = xml.dom.minidom.parseString(pm_nogeom_kml)
    assert None == kml.bbox.GetPlacemarkBBOX(pm_nogeom_node)


def suite():
  suite = unittest.TestSuite()
  suite.addTest(TestGetCoordinatesBBOX())
  suite.addTest(TestGetPlacemarkBBOX())
  suite.addTest(TestNoGeomPlacemarkBBOX())
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())

