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
import kml.genxml
import kml.kmlparse
import xml.dom.minidom


class BasicSimpleElementTestCase(unittest.TestCase):
  def runTest(self):
    xml = kml.genxml.SimpleElement('mytag','mycontent')
    assert xml == '<mytag>mycontent</mytag>\n', 'mytag SimpleElement failed'


class BasicSimpleElementListTestCase(unittest.TestCase):
  def runTest(self):
    nvp_list = [['a','0'],['b','1'],['c','2']]
    xml = kml.genxml.SimpleElementList(nvp_list)
    assert xml == '<a>0</a>\n<b>1</b>\n<c>2</c>\n', 'abc element list failed'


class BasicElementAttributesTestCase(unittest.TestCase):
  def runTest(self):
    nvp_list = [['a','0'],['b','1'],['c','2']]
    attrs = kml.genxml.ElementAttributes(nvp_list)
    assert attrs == ' a="0" b="1" c="2"', 'abc attribute list failed'


class EmptyComplexElementTestCase(unittest.TestCase):
  def runTest(self):
    empty = kml.genxml.ComplexElement('empty',None,None,None,None)
    assert empty == '<empty/>\n', 'empty complex element failed'


basic_complex_xml = ['<xyz>\n',
                     '<aa>00</aa>\n',
                     '<bb>11</bb>\n',
                     '<cc>22</cc>\n',
                     '<hi><ho>there</ho></hi>\n',
                     '<bye/>\n',
                     '</xyz>\n']


class BasicComplexElementTestCase(unittest.TestCase):
  def runTest(self):
    elements = [['aa','00'],['bb','11'],['cc','22']]
    children = '<hi><ho>there</ho></hi>\n<bye/>\n'
    xml = kml.genxml.ComplexElement('xyz', None, None, elements, children)
    assert xml == "".join(basic_complex_xml), 'xyz complex element failed'

class AbstractViewTestCase(unittest.TestCase):
  def runTest(self):
    lookat = kml.genxml.LookAt()
    folder = kml.genxml.Folder()
    folder.AbstractView = lookat.xml()
    camera = kml.genxml.Camera()
    placemark = kml.genxml.Placemark()
    placemark.AbstractView = camera.xml()

class ViewVolumeTestCase(unittest.TestCase):
  def runTest(self):
    viewvolume = kml.genxml.ViewVolume()
    viewvolume.leftFov = -66.7
    viewvolume.rightFov = 63.2
    viewvolume.bottomFov = -33.33
    viewvolume.topFov = 25.26
    viewvolume.near = 100.101
    vv_node = xml.dom.minidom.parseString(viewvolume.xml())
    assert -66.7 == float(kml.kmlparse.GetSimpleElementText(vv_node, 'leftFov'))
    assert 63.2 == float(kml.kmlparse.GetSimpleElementText(vv_node, 'rightFov'))
    assert -33.33 == float(kml.kmlparse.GetSimpleElementText(vv_node, 'bottomFov'))
    assert 25.26 == float(kml.kmlparse.GetSimpleElementText(vv_node, 'topFov'))
    assert 100.101 == float(kml.kmlparse.GetSimpleElementText(vv_node, 'near'))

class ImagePyramidTestCase(unittest.TestCase):
  def runTest(self):
    imagepyramid = kml.genxml.ImagePyramid()
    imagepyramid.tileSize = 513
    imagepyramid.maxWidth = 12345
    imagepyramid.maxHeight = 67890
    ip_node = xml.dom.minidom.parseString(imagepyramid.xml())
    assert 513 == int(kml.kmlparse.GetSimpleElementText(ip_node, 'tileSize'))
    assert 12345 == int(kml.kmlparse.GetSimpleElementText(ip_node, 'maxWidth'))
    assert 67890 == int(kml.kmlparse.GetSimpleElementText(ip_node, 'maxHeight'))

def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicSimpleElementTestCase())
  suite.addTest(BasicSimpleElementListTestCase())
  suite.addTest(BasicElementAttributesTestCase())
  suite.addTest(EmptyComplexElementTestCase())
  suite.addTest(BasicComplexElementTestCase())
  suite.addTest(AbstractViewTestCase())
  suite.addTest(ViewVolumeTestCase())
  suite.addTest(ImagePyramidTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())
