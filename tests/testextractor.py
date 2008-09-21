#!/usr/bin/env python

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
import gdal
import kml.extractor


def VerifyDimensions(imagefile, wid, ht):
  ds = gdal.Open(imagefile)
  if wid == ds.RasterXSize and ht == ds.RasterYSize:
    return True
  return False


class SimpleJPEGExtractorTestCase(unittest.TestCase):
  def setUp(self):
    self.wid = self.ht = 256
    self.ex = kml.extractor.Extractor('NASA_KSC.jpg',self.wid,self.ht,'JPEG')
    self.tempname = tempfile.mktemp()
    self.tempnamej = '%s.JPEG' % self.tempname
  def testNW(self):
    self.ex.Extract(0,0,256,256,self.tempname)
    good = VerifyDimensions(self.tempnamej, self.wid, self.ht)
    assert good, 'NW wrong dimensions'
  def testNE(self):
    self.ex.Extract(256,0,256,256,self.tempname)
    good = VerifyDimensions(self.tempnamej, self.wid, self.ht)
    assert good, 'NE wrong dimensions'
  def testSW(self):
    self.ex.Extract(0,256,256,256,self.tempname)
    good = VerifyDimensions(self.tempnamej, self.wid, self.ht)
    assert good, 'SW wrong dimensions'
  def testSE(self):
    self.ex.Extract(256,256,256,256,self.tempname)
    good = VerifyDimensions(self.tempnamej, self.wid, self.ht)
    assert good, 'SE wrong dimensions'
  def tearDown(self):
    os.unlink(self.tempnamej)


class SimplePNGExtractorTestCase(unittest.TestCase):
  def setUp(self):
    self.wid = self.ht = 256
    self.ex = kml.extractor.Extractor('NASA_KSC.jpg',self.wid,self.ht,'PNG')
    self.tempname = tempfile.mktemp()
    self.tempnamep = '%s.PNG' % self.tempname
  def testNW(self):
    self.ex.Extract(0,0,256,256,self.tempname)
    good = VerifyDimensions(self.tempnamep, self.wid, self.ht)
    assert good, 'NW wrong dimensions'
  def testNE(self):
    self.ex.Extract(256,0,256,256,self.tempname)
    good = VerifyDimensions(self.tempnamep, self.wid, self.ht)
    assert good, 'NE wrong dimensions'
  def testSW(self):
    self.ex.Extract(0,256,256,256,self.tempname)
    good = VerifyDimensions(self.tempnamep, self.wid, self.ht)
    assert good, 'SW wrong dimensions'
  def testSE(self):
    self.ex.Extract(256,256,256,256,self.tempname)
    good = VerifyDimensions(self.tempnamep, self.wid, self.ht)
    assert good, 'SE wrong dimensions'
  def tearDown(self):
    os.unlink(self.tempnamep)


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

