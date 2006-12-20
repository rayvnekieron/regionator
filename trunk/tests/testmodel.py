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
    (lon,lat) = model.Location()
    assert lon == -122.405843291645, 'bad longitude'
    assert lat == 37.802415973264, 'bad latitude'


class SimpleModelSetTestCase(unittest.TestCase):
  def runTest(self):
    modelset = kml.model.ModelSet('.')
    modelset.FindAndParse()

    locations = modelset.Locations()
    print len(locations)
    assert len(locations) == 2, 'modelset Locations failed'

    model = modelset.GetModel('coit')
    assert model, 'modelset GetModel failed'
    assert model.Kmz() == './coit.kmz', 'model Kmz failed'

    model = modelset.GetModel('London_house')
    assert model, 'modelset GetModel failed'
    assert model.Kmz() == './London_house.kmz', 'model Kmz failed'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleModelTestCase())
  suite.addTest(SimpleModelSetTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

