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
import kml.superoverlay
import kml.checklinks
import kml.checkregions

class BasicSuperOverlayTestCase(unittest.TestCase):
  def runTest(self):
    argv = []
    argv.append('-i')
    argv.append('NASA_KSC.jpg')
    tmpdir = tempfile.mkdtemp()
    dir = os.path.join(tmpdir, 'dir')
    argv.append('-d')
    argv.append(dir)
    argv.append('-k')
    argv.append('go.kml')
    superoverlay = kml.superoverlay.SuperOverlayConfig(argv)
    status = kml.superoverlay.CreateSuperOverlay(superoverlay)
    assert True == status
    kml1 = os.path.join(dir, '1.kml')
    assert 0 == kml.checklinks.CheckLinks(['-rk', '-u', kml1])
    region_handler = kml.checkregions.CheckRegions('', kml1)
    assert 0 == region_handler.Status()

    for file in os.listdir(dir):
      os.unlink(os.path.join(dir, file))
    os.rmdir(dir)
    os.rmdir(tmpdir)

def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicSuperOverlayTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

