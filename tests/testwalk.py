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


class SimpleWalkTestCase(unittest.TestCase):
  def runTest(self):
    class MyNodeHandler(kml.walk.KMLNodeHandler):
      def __init__(self):
        self.__count = 0
      def GetCount(self):
        return self.__count
      def HandleNode(self, node, llab, lod):
        self.__count += 1
    
    my_node_handler = MyNodeHandler()
    hierarchy = kml.walk.KMLHierarchy()
    hierarchy.SetNodeHandler(my_node_handler)
    # generated in testpm.py from placemarks.kml
    hierarchy.Walk('pmroot.kml')
    assert my_node_handler.GetCount() == 33,'simple walk failed'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleWalkTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())


