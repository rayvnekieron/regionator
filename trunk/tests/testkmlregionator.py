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
import os.path
import tempfile
import unittest
import kml.kmlregionator


class KMLRegionatorPlacemarksTestCase(unittest.TestCase):
  def setUp(self):
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

  def testFiles(self):
    assert os.access(self.rootkml, os.F_OK)
    kml1 = os.path.join(self.dir, '1.kml')
    assert os.access(kml1, os.F_OK)
    kml50 = os.path.join(self.dir, '50.kml')
    assert os.access(kml50, os.F_OK)
    assert len(os.listdir(self.dir)) == 50

  # TODO: verify all Placemarks in hierarchy against input
  #       verify minLodPixels=minpx
  #       verify no .kml has > maxper Placemarks
  #       verify proper None return if dir doesn't exist
  #       verify proper None return if inputkml fails to parse
  #       verify Style and Schema

def suite():
  suite = unittest.TestSuite()
  suite.addTest(KMLRegionatorPlacemarksTestCase("testFiles"))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

