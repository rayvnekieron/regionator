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
    # generated in testpm.py from placemarks.kml
    hierarchy.Walk('pmroot.kml')
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


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleWalkTestCase())
  suite.addTest(NoNodeHandlerTestCase())
  suite.addTest(NonExistentUrlTestCase())
  suite.addTest(BasicWalkTestCase("testNoChildren"))
  suite.addTest(BasicWalkTestCase("testOneChild"))
  suite.addTest(BasicWalkTestCase("testMissingChild"))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())


