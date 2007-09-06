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

import kml.feature
import xml.dom.minidom

empty_kml = '<kml/>'
kml_placemark = '<kml><Placemark/></kml>'
placemark = '<Placemark/>'
kml_folder = '<kml><Folder><Placemark/></Folder></kml>'
kml_doc = '<kml><Document><Placemark/></Document></kml>'
kml_fpp = '<Folder><Placemark/><Placemark/></Folder>'
kml_dng = '<Document><NetworkLink/><GroundOverlay/></Document>'
ffp = '<Folder><Folder><Placemark/></Folder></Folder>'

class PrintFeaturesTestCase(unittest.TestCase):
  def runTest(self):
    doc = xml.dom.minidom.parseString(placemark)
    feature_list = kml.feature.GetFeatureElementsInDoc(doc)
    str = kml.feature.PrintFeaturesToString(doc, feature_list, 0)
    assert 'Placemark' == str

    doc = xml.dom.minidom.parseString(kml_folder)
    feature_list = kml.feature.FindFeaturesInDoc(doc)
    assert 1 == len(feature_list)
    str = kml.feature.PrintFeaturesToString(doc, feature_list, 0)
    lines = str.split('\n')
    assert 'Folder' == lines[0]
    assert ' Placemark' == lines[1]

    doc = xml.dom.minidom.parseString(ffp)
    feature_list = kml.feature.FindFeaturesInDoc(doc)
    assert 1 == len(feature_list)
    str = kml.feature.PrintFeaturesToString(doc, feature_list, 0)
    lines = str.split('\n')
    assert 'Folder' == lines[0]
    assert ' Folder' == lines[1]
    assert '  Placemark' == lines[2]

class GetFeaturesTestCase(unittest.TestCase):
  def runTest(self):
    doc = xml.dom.minidom.parseString(placemark)
    feature_list = kml.feature.GetFeatureElementsInDoc(doc)
    assert 1 == len(feature_list)
    assert 'Placemark' == feature_list[0].tagName

    doc = xml.dom.minidom.parseString(kml_placemark)
    feature_list = kml.feature.FindFeaturesInDoc(doc)
    assert 1 == len(feature_list)
    assert 'Placemark' == feature_list[0].tagName

    doc = xml.dom.minidom.parseString(kml_folder)
    feature_list = kml.feature.FindFeaturesInDoc(doc)
    assert 1 == len(feature_list)
    assert 'Folder' == feature_list[0].tagName

    doc = xml.dom.minidom.parseString(kml_doc)
    feature_list = kml.feature.FindFeaturesInDoc(doc)
    assert 1 == len(feature_list)
    assert 'Document' == feature_list[0].tagName

    doc = xml.dom.minidom.parseString(kml_fpp)
    feature_list = kml.feature.FindFeaturesInDoc(doc)
    assert 1 == len(feature_list)
    assert 'Folder' == feature_list[0].tagName

class IsFeatureTestCase(unittest.TestCase):
  def runTest(self):
    doc = xml.dom.minidom.parseString('<Placemark/>')
    placemark_node = doc.getElementsByTagName('Placemark')[0]
    assert True == kml.feature.IsFeature(placemark_node)

    doc = xml.dom.minidom.parseString('<Folder/>')
    folder_node = doc.getElementsByTagName('Folder')[0]
    assert True == kml.feature.IsFeature(folder_node)
    assert True == kml.feature.IsContainer(folder_node)

    doc = xml.dom.minidom.parseString('<ScreenOverlay/>')
    so_node = doc.getElementsByTagName('ScreenOverlay')[0]
    assert True == kml.feature.IsFeature(so_node)
    assert True == kml.feature.IsOverlay(so_node)

def suite():
  suite = unittest.TestSuite()
  suite.addTest(IsFeatureTestCase())
  suite.addTest(GetFeaturesTestCase())
  suite.addTest(PrintFeaturesTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())
