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

class LinearRingTestCase(unittest.TestCase):
  def runTest(self):
    clockwise_coords = '0,0 0,1 1,1 1,0 0,0'
    counterclockwise_coords = '0,0 1,0 1,1 0,1 0,0'
    first_not_last_coords = '0,0 1,1 2,2 3,3 4,4'
    lr = kml.genxml.LinearRing()
    
    lr.Set_coordinates(clockwise_coords)
    assert True == lr.is_clockwise()
    lr.reverse_winding_order()
    assert False == lr.is_clockwise()
    
    lr.Set_coordinates(counterclockwise_coords)
    assert False == lr.is_clockwise()
    lr.reverse_winding_order()
    assert True == lr.is_clockwise()

    lr.Set_coordinates(first_not_last_coords)
    assert False == lr.is_clockwise()
    assert False == lr.first_equals_last()
    lr.close_loop()
    assert True == lr.first_equals_last()
    lr.close_loop() # Calling a second time is no-op
    lr_node = xml.dom.minidom.parseString(lr.xml())
    lr_coords = kml.kmlparse.GetSimpleElementText(lr_node, 'coordinates')
    good = ' '.join(['%0.6f,%0.6f,%0.6f' % (x,x,0) for x in (0,1,2,3,4,0)])
    assert good == lr_coords
    

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

class PhotoOverlayTestCase(unittest.TestCase):
  def runTest(self):
    href = 'http://goo.com/big/l$[level]/r$[x]-c$[y]'
    shape = 'sphere'
    roll = -12.34
    drawOrder = 14

    photooverlay = kml.genxml.PhotoOverlay()
    viewvolume = kml.genxml.ViewVolume()
    viewvolume.leftFov = -66.7
    viewvolume.rightFov = 63.2
    viewvolume.bottomFov = -33.33
    viewvolume.topFov = 25.26
    viewvolume.near = 100.101
    photooverlay.ViewVolume = viewvolume.xml()
    imagepyramid = kml.genxml.ImagePyramid()
    imagepyramid.tileSize = 513
    imagepyramid.maxWidth = 12345
    imagepyramid.maxHeight = 67890
    photooverlay.ImagePyramid = imagepyramid.xml()
    photooverlay.Point = kml.genkml.Point(111,22)
    photooverlay.shape = shape
    photooverlay.roll = roll
    # The Overlay-ness of PhotoOverlay:
    icon = kml.genxml.Icon()
    icon.href = href
    photooverlay.Icon = icon.xml()
    photooverlay.drawOrder = drawOrder
    # The Feature-ness of PhotoOverlay:
    photooverlay.name = 'big photo'
    # The Object-ness of PhotoOverlay:
    photooverlay.id = 'my-big-photo'

    po_node = xml.dom.minidom.parseString(photooverlay.xml())
    assert roll == float(kml.kmlparse.GetSimpleElementText(po_node, 'roll'))
    assert shape == kml.kmlparse.GetSimpleElementText(po_node, 'shape')
    assert drawOrder == int(
        kml.kmlparse.GetSimpleElementText(po_node, 'drawOrder'))
    icon_node = kml.kmlparse.GetFirstChildElement(po_node, 'Icon')
    icon = kml.kmlparse.ParseIcon(icon_node)
    assert href == icon.href

class DataTestCase(unittest.TestCase):
  def runTest(self):
    data = kml.genxml.Data()
    data.name = 'par'
    data.displayName = 'The par is'
    data.value = 4
    data_node = xml.dom.minidom.parseString(data.xml())
    assert data.displayName == kml.kmlparse.GetSimpleElementText(data_node, 'displayName')
    assert data.value == int(kml.kmlparse.GetSimpleElementText(data_node, 'value'))

class ExtendedDataTestCase(unittest.TestCase):
  def runTest(self):
    ed = kml.genxml.ExtendedData()
    name = 'busNumber'
    display_name = 'Bus Number'
    value = 30
    data_kml = kml.genkml.Data(name, display_name, value)
    ed.Add_Data(data_kml)
    ed_node = xml.dom.minidom.parseString(ed.xml())
    data_node = kml.kmlparse.GetFirstChildElement(ed_node, 'Data')
    assert display_name == kml.kmlparse.GetSimpleElementText(data_node, 'displayName')
    assert value == int(kml.kmlparse.GetSimpleElementText(data_node, 'value'))

def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicSimpleElementTestCase())
  suite.addTest(BasicSimpleElementListTestCase())
  suite.addTest(BasicElementAttributesTestCase())
  suite.addTest(EmptyComplexElementTestCase())
  suite.addTest(BasicComplexElementTestCase())
  suite.addTest(LinearRingTestCase())
  suite.addTest(AbstractViewTestCase())
  suite.addTest(ViewVolumeTestCase())
  suite.addTest(ImagePyramidTestCase())
  suite.addTest(PhotoOverlayTestCase())
  suite.addTest(DataTestCase())
  suite.addTest(ExtendedDataTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())
