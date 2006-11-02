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



# Simple test of Tile extraction

import unittest
import sys
import os

import gdal

import kml.extractor

in_image = sys.argv[1]

"""
ex = kml.extractor.Extractor(in_image,256,256,'JPEG')
ex.Extract(0,0,256,256,'0')
ex.Extract(256,0,256,256,'1')
ex.Extract(0,256,256,256,'2')
ex.Extract(256,256,256,256,'3')
"""


def VerifyDimensions(imagefile, wid, ht):
  ds = gdal.Open(imagefile)
  if wid == ds.RasterXSize and ht == ds.RasterYSize:
    return True
  return False


class SimpleJPEGExtractorTestCase(unittest.TestCase):
  def setUp(self):
    self.wid = self.ht = 256
    self.ex = kml.extractor.Extractor(in_image,self.wid,self.ht,'JPEG')
  def testNW(self):
    self.ex.Extract(0,0,256,256,'x')
    assert VerifyDimensions('x.JPEG', self.wid, self.ht), 'NW wrong dimensions'
  def testNE(self):
    self.ex.Extract(256,0,256,256,'x')
    assert VerifyDimensions('x.JPEG', self.wid, self.ht), 'NE wrong dimensions'
  def testSW(self):
    self.ex.Extract(0,256,256,256,'x')
    assert VerifyDimensions('x.JPEG', self.wid, self.ht), 'SW wrong dimensions'
  def testSE(self):
    self.ex.Extract(256,256,256,256,'x')
    assert VerifyDimensions('x.JPEG', self.wid, self.ht), 'SE wrong dimensions'
  def tearDown(self):
    os.unlink('x.JPEG')


class SimplePNGExtractorTestCase(unittest.TestCase):
  def setUp(self):
    self.wid = self.ht = 256
    self.ex = kml.extractor.Extractor(in_image,self.wid,self.ht,'PNG')
  def testNW(self):
    self.ex.Extract(0,0,256,256,'x')
    assert VerifyDimensions('x.PNG', self.wid, self.ht), 'NW wrong dimensions'
  def testNE(self):
    self.ex.Extract(256,0,256,256,'x')
    assert VerifyDimensions('x.PNG', self.wid, self.ht), 'NE wrong dimensions'
  def testSW(self):
    self.ex.Extract(0,256,256,256,'x')
    assert VerifyDimensions('x.PNG', self.wid, self.ht), 'SW wrong dimensions'
  def testSE(self):
    self.ex.Extract(256,256,256,256,'x')
    assert VerifyDimensions('x.PNG', self.wid, self.ht), 'SE wrong dimensions'
  def tearDown(self):
    os.unlink('x.PNG')


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleJPEGExtractorTestCase("testNW"))
  suite.addTest(SimpleJPEGExtractorTestCase("testSW"))
  suite.addTest(SimpleJPEGExtractorTestCase("testSE"))
  suite.addTest(SimpleJPEGExtractorTestCase("testNE"))
  suite.addTest(SimplePNGExtractorTestCase("testNW"))
  suite.addTest(SimplePNGExtractorTestCase("testSW"))
  suite.addTest(SimplePNGExtractorTestCase("testSE"))
  suite.addTest(SimplePNGExtractorTestCase("testNE"))
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())

