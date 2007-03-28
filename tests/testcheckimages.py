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
import kml.checkimages
import kml.kmlregionator
import kml.walk

class NullTestCase(unittest.TestCase):
  def runTest(self):
    # Create an instance with no arguments
    image_checker = kml.checkimages.ImageCheckingNodeHandler('')
    # Do nothing and status should be 0
    assert 0 == image_checker.Status()

class BasicTestCase(unittest.TestCase):
  def setUp(self):
    argv = []
    argv.append('-i')
    argv.append('NASA_KSC.jpg')
    argv.append('-k')
    argv.append('ksc-llb-3.kml')
    argv.append('-d')
    self.tmpdir = tempfile.mkdtemp()
    self.sodir = os.path.join(self.tmpdir, 'dir')
    argv.append(self.sodir)
    superoverlay = kml.superoverlay.SuperOverlayConfig(argv)
    status = kml.superoverlay.CreateSuperOverlay(superoverlay)

  def tearDown(self):
    for file in os.listdir(self.sodir):
      os.unlink(os.path.join(self.sodir, file))
    os.rmdir(self.sodir)
    os.rmdir(self.tmpdir)

  def testStatus(self):
    kml1 = os.path.join(self.sodir, '1.kml')
    opts = ['-r']
    image_checking_handler = kml.checkimages.ImageCheckingNodeHandler(opts)
    hier = kml.walk.KMLHierarchy()
    hier.SetNodeHandler(image_checking_handler)
    hier.Walk(kml1)
    (max_size,max_url,min_size,min_url,count,total) = \
                                         image_checking_handler.Statistics()
    assert 33938 == max_size
    assert '1.JPEG' == os.path.basename(max_url)
    assert 5259 == min_size
    assert '15.JPEG' == os.path.basename(min_url)
    assert 24 == count
    assert 481658 == total


def suite():
  suite = unittest.TestSuite()
  suite.addTest(NullTestCase())
  suite.addTest(BasicTestCase('testStatus'))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

