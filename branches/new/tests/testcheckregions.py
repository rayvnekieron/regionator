#!/usr/bin/env python

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
import kml.checkregions
import kml.kmlregionator

class NullTestCase(unittest.TestCase):
  def runTest(self):
    # Create an instance with no arguments
    region_checker = kml.checkregions.RegionCheckingNodeHandler('')
    # Do nothing and check sane status
    assert 0 == region_checker.Status()

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

  def testCheckRegions(self):
    # MakeRootKML basically expects a relative dir but we hand it
    # an absolute path in setUp.  So we hop over it here.
    kml1 = os.path.join(self.dir, '1.kml')
    # This NetworkLink hierarchy is known to have no errors
    region_handler = kml.checkregions.CheckRegions('',kml1)
    assert 0 == region_handler.Status()

class BadRegionFileTestCase(unittest.TestCase):
  def runTest(self):
    region_handler = kml.checkregions.CheckRegions([], 'badregions.kml')
    print region_handler.Status()
    assert 20 == region_handler.Status()

def suite():
  suite = unittest.TestSuite()
  suite.addTest(NullTestCase())
  suite.addTest(BasicTestCase("testCheckRegions"))
  suite.addTest(BadRegionFileTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

