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
import os
import tempfile

import kml.placemarkregionator
import kml.region
import kml.qidboxes
import kml.dashboard


class BasicPlacemarkRegionatorTestCase(unittest.TestCase):
  def setUp(self):
   self.__dir = tempfile.mktemp()
   self.__root = tempfile.mktemp()
   self.__pmr = kml.placemarkregionator.PlacemarkRegionator()
   self.__pmr.SetVerbose(False)

  def tearDown(self):
    for name in os.listdir(self.__dir):
      os.unlink(os.path.join(self.__dir, name))
    os.rmdir(self.__dir)
    os.unlink(self.__root)

  def testRegionate7(self):
   kmlfile = 'placemarks.kml'
   per = 7
   rtor = self.__pmr.Regionate(kmlfile,128,per,self.__root,self.__dir)
   assert len(rtor.QidList()) == 32, 'basic ptor7 qidlist bad'
   assert rtor.RegionCount() == 32, 'basic ptor7 region count bad'
   assert rtor.MaxDepth() == 5, 'basic ptor7 max depth bad'

  def testRegionate2(self):
   kmlfile = 'placemarks.kml'
   per = 2
   rtor = self.__pmr.Regionate(kmlfile,128,per,self.__root,self.__dir)
   assert len(rtor.QidList()) == 82, 'basic ptor2 qidlist bad'
   assert rtor.RegionCount() == 82, 'basic ptor2 region count bad'
   assert rtor.MaxDepth() == 8, 'basic ptor2 max depth bad'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicPlacemarkRegionatorTestCase("testRegionate7"))
  suite.addTest(BasicPlacemarkRegionatorTestCase("testRegionate2"))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

