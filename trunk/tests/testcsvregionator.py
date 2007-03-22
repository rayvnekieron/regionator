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
    rtor = kml.csvregionator.RegionateCSV(csvfile,
                                          codec,
                                          min_lod_pixels,
                                          max_per,
                                          root,
                                          odir,
                                          verbose)

    kml1 = os.path.join(odir, '1.kml')
    assert os.access(kml1, os.R_OK)

    assert 206 == len(os.listdir(odir))

    region_handler = kml.checkregions.CheckRegions('', kml1)
    assert 0 == region_handler.Status()

    for file in os.listdir(odir):
      os.unlink(os.path.join(odir, file))
    os.rmdir(odir)


def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicCsvRegionatorTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

