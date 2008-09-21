#!/usr/bin/env python
# coding=UTF-8
#  See http://www.python.org/dev/peps/pep-0263/
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
import tempfile
import unittest
import kml.csvregionator
import kml.checkregions


class BasicCsvRegionatorTestCase(unittest.TestCase):
  def runTest(self):
    csvfile = 'gec.csv'
    codec = 'latin_1' # Encoding of input file (output will be utf-8)
    min_lod_pixels = 256
    max_per = 8
    root = None # Don't make a root.kml
    odir = tempfile.mkdtemp()
    verbose = False
    global_styleUrl = None
    rtor = kml.csvregionator.RegionateCSV(csvfile,
                                          codec,
                                          min_lod_pixels,
                                          max_per,
                                          root,
                                          odir,
                                          verbose,
                                          global_styleUrl)

    kml1 = os.path.join(odir, '1.kml')
    assert os.access(kml1, os.R_OK)

    assert 206 == len(os.listdir(odir))

    region_handler = kml.checkregions.CheckRegions('', kml1)
    assert 0 == region_handler.Status()

    for file in os.listdir(odir):
      os.unlink(os.path.join(odir, file))
    os.rmdir(odir)


class StyledCsvRegionatorTestCase(unittest.TestCase):
  def runTest(self):
    csvfile = 'mixed-styles.csv'
    codec = 'UTF-8'
    min_lod_pixels = 256
    max_per = 8
    root = None # Don't make a root.kml
    verbose = False
    global_styleUrls = [None, '#globalStyle']
    for i in range(2): # Test creation w/ and w/o cmd line global styleUrls
      odir = tempfile.mkdtemp()
      rtor = kml.csvregionator.RegionateCSV(csvfile,
                                            codec,
                                            min_lod_pixels,
                                            max_per,
                                            root,
                                            odir,
                                            verbose,
                                            global_styleUrls[i])
      kml1 = os.path.join(odir, '1.kml')
      assert os.access(kml1, os.R_OK)
      kml1_data = open(kml1, 'r').read()
      assert 1 == kml1_data.count('#tomStyle')
      assert 1 == kml1_data.count('#harryStyle')
      if i == 0: # No global style
        assert 0 == kml1_data.count('#globalStyle')
      else: # Second placemark should have global styleUrl
        assert  1 == kml1_data.count('#globalStyle')
      for file in os.listdir(odir):
        os.unlink(os.path.join(odir, file))
      os.rmdir(odir)


class CodecCsvRegionatorTestCase(unittest.TestCase):
  # Codecs aren't being tested anywhere else? Put a test here to make sure it's
  # doing the right thing.
  def runTest(self):
    csvfile = 'utf8.csv'
    codecs = ('utf-8', 'latin_1')
    min_lod_pixels = 256
    max_per = 8
    root = None # Don't make a root.kml
    verbose = False
    global_styleUrl = None
    for codec in codecs:
      odir = tempfile.mkdtemp()
      rtor = kml.csvregionator.RegionateCSV(csvfile,
                                            codec,
                                            min_lod_pixels,
                                            max_per,
                                            root,
                                            odir,
                                            verbose,
                                            global_styleUrl)

      kml1 = os.path.join(odir, '1.kml')
      assert os.access(kml1, os.R_OK)

      kmldata = open(kml1, 'r').read()
      assert 0 < len(kmldata)
      utf8_name_str = '<name><![CDATA[ὕαλον ϕαγεῖν]]></name>'

      if codec == 'utf-8':
        assert -1 != kmldata.find(utf8_name_str)
      elif codec == 'latin_1':
        assert -1 == kmldata.find(utf8_name_str)
    
      region_handler = kml.checkregions.CheckRegions('', kml1)
      assert 0 == region_handler.Status()

      for file in os.listdir(odir):
        os.unlink(os.path.join(odir, file))
      os.rmdir(odir)

class BasicParseCsvLineTestCase(unittest.TestCase):
  def runTest(self):
    csv_line = '10336|46.7559458035|6.95348450281|Chatonnaye|www.chatonnaye.ch'
    (score, lon, lat, name, description, style_url) = \
      kml.csvregionator.ParseCsvLine(csv_line, 'utf-8')
    # assert 10366 == score
    # assert 46.7559458035 == lon
    # assert 6.95348450281 == lat
    assert 'Chatonnaye' == name
    assert 'www.chatonnaye.ch' == description
    assert None == style_url

def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicCsvRegionatorTestCase())
  suite.addTest(StyledCsvRegionatorTestCase())
  suite.addTest(CodecCsvRegionatorTestCase())
  suite.addTest(BasicParseCsvLineTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())
