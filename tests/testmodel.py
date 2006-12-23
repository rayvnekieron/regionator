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

import kml.model


class SimpleModelTestCase(unittest.TestCase):
  def runTest(self):
    model = kml.model.Model()
    model.Parse('coit.kml')
    (lon,lat) = model.LonLatF()
    assert lon == -122.405843291645, 'bad longitude'
    assert lat == 37.802415973264, 'bad latitude'


class SimpleModelSetTestCase(unittest.TestCase):
  def setUp(self):
    self.__modelset = kml.model.ModelSet('.')
    self.__modelset.FindAndParse()
  def testLocations(self):
    locations = self.__modelset.Locations()
    assert len(locations) == 2, 'modelset Locations failed'
  def testGetModel(self):
    model = self.__modelset.GetModel('coit')
    assert model, 'modelset GetModel failed'
    assert model.Kmz() == './coit.kmz', 'model Kmz failed'
    model = self.__modelset.GetModel('London_house')
    assert model, 'modelset GetModel failed'
    assert model.Kmz() == './London_house.kmz', 'model Kmz failed'
  def testIterate(self):
    count = 0
    for model in self.__modelset:
      count += 1
    assert count == 2, 'model iterator failed'

class ModelSetBBOXTestCase(unittest.TestCase):
  def runTest(self):
    modelset = kml.model.ModelSet('.')
    modelset.FindAndParse()
    (n,s,e,w) = modelset.FindBBOX()
    assert n == 51.515803220526, 'bad bbox north'
    assert s == 37.802415973264, 'bad bbox south'
    assert e == -0.114086084916, 'bad bbox east'
    assert w == -122.405843291645, 'bad bbox west'


class SimpleKmzTestCase(unittest.TestCase):
  def setUp(self):
    self.__model = kml.model.Model()
    self.__model.Parse('London_house.kmz')
  def testKmzSize(self):
    assert self.__model.KmzSize() == 24867,'model kmz size bad'
  def testGeometrySize(self):
    geometry = self.__model.GetGeometry()
    assert len(geometry) == 36032,'model geometry size bad'
  def testTexturesTxtSize(self):
    textures_txt = self.__model.ReadFileData('textures.txt')
    assert len(textures_txt) == 180,'model textures.txt size bad'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleModelTestCase())
  suite.addTest(SimpleModelSetTestCase("testLocations"))
  suite.addTest(SimpleModelSetTestCase("testGetModel"))
  suite.addTest(SimpleModelSetTestCase("testIterate"))
  suite.addTest(ModelSetBBOXTestCase())
  suite.addTest(SimpleKmzTestCase("testKmzSize"))
  suite.addTest(SimpleKmzTestCase("testGeometrySize"))
  suite.addTest(SimpleKmzTestCase("testTexturesTxtSize"))
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

