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
import tempfile
import os
import kml.regionator
import kml.kmlregionator
import kml.gatherlinks

class BasicRbNLTestCase(unittest.TestCase):
  def setUp(self):
    # Create a Region-based NetworkLink hierarchy to check
    inputkml = 'placemarks.kml'
    minpx = 256
    maxper = 4
    self.dir = tempfile.mkdtemp()
    verbose = False
    self.rtor = kml.kmlregionator.RegionateKML(inputkml,
                                               minpx,
                                               maxper,
                                               None,
                                               self.dir,
                                               verbose)

  def tearDown(self):
    for file in os.listdir(self.dir):
      os.unlink(os.path.join(self.dir, file))
    os.rmdir(self.dir)

  def testGatherNoLinks(self):
    kml1 = os.path.join(self.dir, '1.kml')
    links = kml.gatherlinks.GatherLinks(['-u', kml1])
    assert 0 == len(links)

  def testGatherRelativeKmlLinks(self):
    kml1 = os.path.join(self.dir, '1.kml')
    links = kml.gatherlinks.GatherLinks(['-k','-r','-u',kml1])
    # The above RnNL hierarchy is known to have files 2.kml ... 50.kml
    filenum = 2
    while filenum <= 50:
      file = os.path.join(self.dir, '%d.kml' % filenum)
      assert links.has_key(file), file
      filenum += 1

class BasicRelativeTestCase(unittest.TestCase):
  def runTest(self):
    links = kml.gatherlinks.GatherLinks(['-h','-k','-r','-u','html.kml'])
    assert 1 == links['../sketchup_building_golden1.png']
    assert 1 == links['../3dwh-logo_en.gif']
    assert 1 == links['../../placemarks/99/1952f8d3e8d27fe065a153e1a3d3359c.jpg']
    assert 3 == len(links)

class BasicAbsoluteTestCase(unittest.TestCase):
  def runTest(self):
    links = kml.gatherlinks.GatherLinks(['-h','-k','-a','-u','html.kml'])
    assert 5 == len(links)
    assert 1 == links['http://sketchup.google.com/support/bin/answer.py?answer=57057&hl=en']
    assert 1 == links['http://sketchup.google.com/support/bin/request.py?contact_type=reportmodel&hl=en&mid=1952f8d3e8d27fe065a153e1a3d3359c']
    assert 1 == links['http://sketchup.google.com/3dwarehouse/search?uq=00986856740277826572&hl=en']
    assert 1 == links['http://sketchup.google.com/3dwarehouse?hl=en']
    assert 1 == links['http://sketchup.google.com/3dwarehouse/details?mid=1952f8d3e8d27fe065a153e1a3d3359c&hl=en']

class NonExistentRootTestCase(unittest.TestCase):
  def runTest(self):
    assert None == kml.gatherlinks.GatherLinks(['-u','no-such-file-or-url'])

def suite(): 
  suite = unittest.TestSuite()
  suite.addTest(BasicRbNLTestCase("testGatherNoLinks"))
  suite.addTest(BasicRbNLTestCase("testGatherRelativeKmlLinks"))
  suite.addTest(BasicRelativeTestCase())
  suite.addTest(BasicAbsoluteTestCase())
  suite.addTest(NonExistentRootTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

