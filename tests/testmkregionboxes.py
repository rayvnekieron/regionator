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

import os
import unittest
import tempfile
import kml.kmlregionator
import kml.qidboxes


class BasicMakeRegionBoxesTestCase(unittest.TestCase):
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

  def testMakeRegionBoxes(self):
    rootkml = os.path.join(self.dir, '1.kml')
    dir = tempfile.mkdtemp()
    outputkml = os.path.join(dir, 'out.kml')
    kml.qidboxes.MakeRegionBoxes(rootkml, outputkml)
    assert os.access(outputkml, os.R_OK)
    os.unlink(outputkml)
    os.rmdir(dir)

def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicMakeRegionBoxesTestCase("testMakeRegionBoxes"))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

