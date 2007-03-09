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
import os
import tempfile
import kml.checklinks
import kml.kmlregionator

class NullTestCase(unittest.TestCase):
  def runTest(self):
    # Create an instance with no arguments
    link_checker = kml.checklinks.LinkCheckingNodeHandler('')
    # Do nothing and status should be 0
    assert 0 == link_checker.Status()

class BasicTestCase(unittest.TestCase):
  def setUp(self):
    # Create a Region-based NetworkLink hierarchy to check
    inputkml = 'placemarks.kml'
    minpx = 256
    maxper = 4
    (fd,self.rootkml) = tempfile.mkstemp()
    os.close(fd)
    self.dir = tempfile.mkdtemp()
    verbose = False
    self.rtor = kml.kmlregionator.RegionateKML(inputkml,
                                               minpx,
                                               maxper,
                                               self.rootkml,
                                               self.dir,
                                               verbose)

  def tearDown(self):
    os.unlink(self.rootkml)
    for file in os.listdir(self.dir):
      os.unlink(os.path.join(self.dir, file))
    os.rmdir(self.dir)

  def testCheckLinksOnRelativeKml(self):
    # MakeRootKML basically expects a relative dir but we hand it
    # an absolute path in setUp.  So we hop over it here.
    kml1 = os.path.join(self.dir, '1.kml')
    status = kml.checklinks.CheckLinks(['-k','-r'], kml1)
    assert 0 == status

  def testLinkCheckerOnRelativeKml(self):
    # Set up LinkCheckingNodeHandler directly to dig out its various fields
    link_checker = kml.checklinks.LinkCheckingNodeHandler(['-k','-r'])
    hier = kml.walk.KMLHierarchy()
    hier.SetNodeHandler(link_checker)
    hier.Walk(os.path.join(self.dir, '1.kml'))
    assert 50 == link_checker.node_count
    assert 49 == link_checker.kml_link_count
    assert 0 == link_checker.html_link_count
    assert 49 == link_checker.relative_link_count
    assert 0 == link_checker.absolute_link_count
    assert 0 == link_checker.empty_link_count

class BasicHtmlTestCase(unittest.TestCase):
  def runTest(self):
    link_checker = kml.checklinks.LinkCheckingNodeHandler(['-h','-a'])
    hier = kml.walk.KMLHierarchy()
    hier.SetNodeHandler(link_checker)
    hier.Walk('html.kml')
    assert 8 == link_checker.html_link_count
    assert 1 == link_checker.empty_link_count
    assert 0 == link_checker.Status()

def suite():
  suite = unittest.TestSuite()
  suite.addTest(NullTestCase())
  suite.addTest(BasicTestCase("testCheckLinksOnRelativeKml"))
  suite.addTest(BasicTestCase("testLinkCheckerOnRelativeKml"))
  suite.addTest(BasicHtmlTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

