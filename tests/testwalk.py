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

import sys
import xml.dom.minidom
import kml.walk
import kml.genxml

class NodeCounter(kml.walk.KMLNodeHandler):
  def __init__(self):
    self.__count = 0
  def GetCount(self):
    return self.__count
  def HandleNode(self, href, node, llab, lod):
    self.__count += 1

class SimpleWalkTestCase(unittest.TestCase):
  def runTest(self):
    
    node_counter = NodeCounter()
    hierarchy = kml.walk.KMLHierarchy()
    hierarchy.SetNodeHandler(node_counter)
    # generated in testpm2.py from placemarks.kml
    assert True == hierarchy.Walk('pm2root.kml')
    assert node_counter.GetCount() == 33,'simple walk failed'

class NoNodeHandlerTestCase(unittest.TestCase):
  def runTest(self):
    walker = kml.walk.KMLHierarchy()
    # foo.kml exists and parses, but no KMLNodeHandler was set:
    assert False == walker.Walk('foo.kml')

class NonExistentUrlTestCase(unittest.TestCase):
  def runTest(self):
    walker = kml.walk.KMLHierarchy()
    assert False == walker.Walk('this-does-not-exist')

class BasicWalkTestCase(unittest.TestCase):
  def setUp(self):
    self.node_counter = NodeCounter()
    self.walker = kml.walk.KMLHierarchy()
    self.walker.SetNodeHandler(self.node_counter)
  def testNoChildren(self):
    # foo.kml exists and parses, but has no NetworkLinks:
    assert True == self.walker.Walk('foo.kml')
  def testOneChild(self):
    # foop.kml exists and parses, and has one NetworkLink
    assert True == self.walker.Walk('foop.kml')
  def testMissingChild(self):
    # walkme.kml exists and parses, and has one missing child NetworkLink
    assert False == self.walker.Walk('walkme.kml')

class GetHtmlLinksTestCase(unittest.TestCase):
  def setUp(self):
    self.html_text = 'text<a href="foo.html">hi</a><img src="goo.jpg"/>more'
  def testGetHref(self):
    link_list = []
    kml.walk.GetLinksOfAttr(self.html_text, 'href', link_list)
    assert 1 == len(link_list)
    assert 'foo.html' == link_list[0]
  def testGetSrc(self):
    link_list = []
    kml.walk.GetLinksOfAttr(self.html_text, 'src', link_list)
    assert 1 == len(link_list)
    assert 'goo.jpg' == link_list[0]
  def testGetHrefAndSrc(self):
    link_list = []
    kml.walk.GetLinksOfAttr(self.html_text, 'href', link_list)
    kml.walk.GetLinksOfAttr(self.html_text, 'src', link_list)
    assert 2 == len(link_list)
    assert 'foo.html' == link_list[0]
    assert 'goo.jpg' == link_list[1]
  def testGetLinksInHtml(self):
    link_list = []
    kml.walk.GetLinksInHtml(self.html_text, link_list)
    assert 2 == len(link_list)
    assert 'foo.html' == link_list[0]
    assert 'goo.jpg' == link_list[1]

class GetLinksInKmlNodeTestCase(unittest.TestCase):
  def runTest(self):
    node = xml.dom.minidom.parse('es-latin1.kml')
    link_list = kml.walk.GetHtmlLinksInNode(node)
    assert 8 == len(link_list)
    assert 'http://sketchup.google.com/3dwarehouse?hl=es' == link_list[0]
    assert './../3dwh-logo_es.gif' == link_list[6]


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleWalkTestCase())
  suite.addTest(NoNodeHandlerTestCase())
  suite.addTest(NonExistentUrlTestCase())
  suite.addTest(BasicWalkTestCase("testNoChildren"))
  suite.addTest(BasicWalkTestCase("testOneChild"))
  suite.addTest(BasicWalkTestCase("testMissingChild"))
  suite.addTest(GetHtmlLinksTestCase("testGetHref"))
  suite.addTest(GetHtmlLinksTestCase("testGetSrc"))
  suite.addTest(GetHtmlLinksTestCase("testGetHrefAndSrc"))
  suite.addTest(GetHtmlLinksTestCase("testGetLinksInHtml"))
  suite.addTest(GetLinksInKmlNodeTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())


