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
import os
import tempfile
import kml.region
import kml.simpleregionator


pm1_kml = "<Placemark><name>1</name></Placemark>"
pm2_kml = "<Placemark><name>2</name></Placemark>"
pm3_kml = "<Placemark><name>3</name></Placemark>"

class BasicSimpleRegionatorTestCase(unittest.TestCase):
  def setUp(self):
    self.__items = []
    self.__items.append(("1.2+3.4", pm1_kml))
    self.__items.append(("2.4+-6.8", pm2_kml))
    self.__items.append(("-33.44+55.66", pm3_kml))
    self.__region = kml.region.Region(60,-7,4,-40,'0')
    self.__dir = tempfile.mkdtemp()

  def tearDown(self):
    for name in os.listdir(self.__dir):
      os.unlink(os.path.join(self.__dir, name))
    os.rmdir(self.__dir)

  def testRegionate2(self):
    (n,s,e,w) = self.__region.NSEW()
    minpx = 123
    per = 2
    rtor = kml.simpleregionator.Regionate(n,s,e,w,
                                          minpx, per,
                                          self.__items,self.__dir,
                                          verbose=False)
    assert len(os.listdir(self.__dir)) == 2, 'basic simple rtor2 file count bad'
    assert rtor.MaxDepth() == 2, 'basic simple rtor2 max depth bad'
    assert rtor.RegionCount() == 2, 'basic simple rtor2 region count bad'
    assert len(rtor.QidList()) == 2, 'basic simple rtor2 qidlist bad'

  def testRegionate1(self):
    (n,s,e,w) = self.__region.NSEW()
    minpx = 123
    per = 1
    rtor = kml.simpleregionator.Regionate(n,s,e,w,
                                          minpx, per,
                                          self.__items,self.__dir,
                                          verbose=False)
    assert len(os.listdir(self.__dir)) == 3, 'basic simple rtor1 file count bad'
    assert rtor.MaxDepth() == 2, 'basic simple rtor1 max depth bad'
    assert rtor.RegionCount() == 3, 'basic simple rtor1 region count bad'
    assert len(rtor.QidList()) == 3, 'basic simple rtor1 qidlist bad'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicSimpleRegionatorTestCase("testRegionate2"))
  suite.addTest(BasicSimpleRegionatorTestCase("testRegionate1"))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

