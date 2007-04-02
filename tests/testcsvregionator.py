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
    odir = tempfile.mkdtemp()
    verbose = False
    global_styleUrls = [None, '#globalStyle']
    for i in range(2):
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
      assert kml1_data.count('#tomStyle') == 1
      assert kml1_data.count('#harryStyle') == 1
      if i == 0: # No global style
        assert kml1_data.count('#globalStyle') == 0
      else: # Second placemark should have global styleUrl
        assert kml1_data.count('#globalStyle') == 1
      for file in os.listdir(odir):
        os.unlink(os.path.join(odir, file))
      os.rmdir(odir)


def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicCsvRegionatorTestCase())
  suite.addTest(StyledCsvRegionatorTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

