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

import kml.kmz

class SimpleKmzTestCase(unittest.TestCase):
  def runTest(self):
    kmz = kml.kmz.Kmz('London_house.kmz')

    ttsize = kmz.GetSize('textures.txt')
    assert ttsize == 180, 'Kmz.GetSize() failed'

    data = kmz.Read('images/GAF_Country_Estates.jpg')
    assert len(data) == 2038, 'Kmz.Read() failed'

    nosize = kmz.GetSize('no_such_file')
    assert nosize == None, 'Kmz.GetSize() of non-existent file failed'

    nodata = kmz.Read('no_such_file')
    assert nodata == None, 'Kmz.Read() of non-existent file failed'

    data = kmz.ReadKml()
    assert len(data) == 818, 'Kmz.ReadKml() failed'


class HttpKmzTestCase(unittest.TestCase):
  def runTest(self):
    kmz = kml.kmz.Kmz('http://regionator.googlecode.com/files/test-158.kmz')

    test_kml_size = kmz.GetSize('test.kml')
    assert test_kml_size == 5321, 'http kmz get size failed'
   

def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleKmzTestCase())
  suite.addTest(HttpKmzTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

