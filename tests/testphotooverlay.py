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

import unittest

import xml.dom.minidom
import kml.photooverlay


class HrefTestCase(unittest.TestCase):
  def runTest(self):
    href = 'a completely invalid href'
    assert False == kml.photooverlay.ValidHref(href)

    href = 'http://host.com/st/gp/$[level]/r$[y]_c$[x].jpg'
    assert True == kml.photooverlay.ValidHref(href)

    href = 'http://host.com/st/gp/$[level]/r$[y]_c$[x].jpg'
    want_href = 'http://host.com/st/gp/0/r2_c1.jpg'
    got_href = kml.photooverlay.ExpandImagePyramidHref(href, 0, 1, 2)
    assert want_href == got_href

class ValidWidHtTestCase(unittest.TestCase):
  def runTest(self):
    assert True == kml.photooverlay.ValidWidHt(2)
    assert True == kml.photooverlay.ValidWidHt(4)
    assert True == kml.photooverlay.ValidWidHt(8)
    assert True == kml.photooverlay.ValidWidHt(16)
    assert True == kml.photooverlay.ValidWidHt(1024)
    assert True == kml.photooverlay.ValidWidHt(65536)
    assert True == kml.photooverlay.ValidWidHt(32768)
    assert True == kml.photooverlay.ValidWidHt(16384)
    assert False == kml.photooverlay.ValidWidHt(-1)
    assert False == kml.photooverlay.ValidWidHt(0)
    assert False == kml.photooverlay.ValidWidHt(1234)
    assert False == kml.photooverlay.ValidWidHt(32769)
    assert False == kml.photooverlay.ValidWidHt(32767)

class CheckPhotoOverlayTestCase(unittest.TestCase):
  def runTest(self):
    doc = xml.dom.minidom.parse('space-needle.kml')
    po_node = kml.kmlparse.GetFirstChildElement(doc, 'PhotoOverlay')
    assert True == kml.photooverlay.CheckPhotoOverlayNode(po_node)

    # A PhotoOverlay with much missing stuff
    po = kml.genxml.PhotoOverlay()
    icon = kml.genxml.Icon()
    po.Icon = icon.xml()
    doc = xml.dom.minidom.parseString(po.xml())
    bad_po = kml.kmlparse.GetFirstChildElement(doc, 'PhotoOverlay')
    assert False == kml.photooverlay.CheckPhotoOverlayNode(bad_po)

class LevelRowColTestCase(unittest.TestCase):
  def runTest(self):
    assert (8, 127, 255) == kml.photooverlay.MaxLevelRowCol(256, 65536, 32768)
    assert (7, 127, 63) == kml.photooverlay.MaxLevelRowCol(256, 16384, 32768)
    assert (0, 0, 0) == kml.photooverlay.MaxLevelRowCol(512, 512, 512)

class CheckPhotoOverlayTestCase(unittest.TestCase):
  def runTest(self):
    doc = xml.dom.minidom.parse('space-needle.kml')
    po_node = kml.kmlparse.GetFirstChildElement(doc, 'PhotoOverlay')
    kml.photooverlay.CheckPhotoOverlay(po_node)

def suite():
  suite = unittest.TestSuite()
  suite.addTest(HrefTestCase())
  suite.addTest(ValidWidHtTestCase())
  suite.addTest(LevelRowColTestCase())
  suite.addTest(CheckPhotoOverlayTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

