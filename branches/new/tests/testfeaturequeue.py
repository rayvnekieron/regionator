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
import kml.featurequeue

class FeatureQueueXAddItemTestCase(unittest.TestCase):
  def runTest(self):
    fq = kml.featurequeue.FeatureQueueX()
    fq.AddItem(('1.1+2.2', '<Placemark/>'))
    fq.AddItem(('-10.9+22.2', '<GroundOverlay/>'))
    fq.AddItem(('80.9+-45.2', '<Folder/>'))
    assert len(fq._Items()) == 3, 'AddItems failed'

class FeatureQueueXAddWeightedItemTestCase(unittest.TestCase):
  def runTest(self):
    fq = kml.featurequeue.FeatureQueueX()
    fq.AddWeightedItem((321, '1.1+2.2', '<Placemark/>'))
    fq.AddWeightedItem((10, '-10.9+22.2', '<GroundOverlay/>'))
    fq.AddWeightedItem((1234, '80.9+-45.2', '<Folder/>'))
    fq._SortItems()
    items = fq._Items()
    assert len(items) == 3, 'AddWeightedItems failed'
    assert items[2][0] == '-10.9+22.2', 'AddWeightedItems sort failed'
    assert items[2][1] == '<GroundOverlay/>', 'AddWeightedItems sort failed'

def suite():
  suite = unittest.TestSuite()
  suite.addTest(FeatureQueueXAddItemTestCase())
  suite.addTest(FeatureQueueXAddWeightedItemTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

