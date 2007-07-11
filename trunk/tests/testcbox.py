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

import kml.coordbox


class MidPointTestCase(unittest.TestCase):
  def runTest(self):
    a = "2,2,0 4,4,0"
    c0 = kml.coordbox.CoordBox()
    c0.AddCoordinates(a)
    (lon,lat) = c0.MidPoint()
    assert lon == 3, 'lon MidPoint wrong'
    assert lat == 3, 'lat MidPoint wrong'

class NSEWTestCase(unittest.TestCase):
  def runTest(self):
    c1 = kml.coordbox.CoordBox()
    n0 = 20
    s0 = 10
    e0 = 40
    w0 = 30
    c1.AddPoint(e0,n0)
    c1.AddPoint(w0,s0)
    c1.AddPoint(32,15)
    (n,s,e,w) = c1.NSEW()
    assert n == n0, 'n NSEW wrong'
    assert s == s0, 's NSEW wrong'
    assert e == e0, 'e NSEW wrong'
    assert w == w0, 'w NSEW wrong'

class SizeTestCase(unittest.TestCase):
  def runTest(self):
    c2 = kml.coordbox.CoordBox()
    c2.AddPoint(10,10)
    c2.AddPoint(20,20)
    size = c2.Size()
    assert size == 10, 'size wrong'

class BasicMidPointTest(unittest.TestCase):
  def runTest(self):
    (lon,lat) = kml.coordbox.MidPoint(20,10,40,20)
    assert 15 == lat
    assert 30 == lon
    
def suite():
  suite = unittest.TestSuite()
  suite.addTest(MidPointTestCase())
  suite.addTest(NSEWTestCase())
  suite.addTest(SizeTestCase())
  suite.addTest(BasicMidPointTest())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

