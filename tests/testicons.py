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
import kml.icons

class BasicRootIconUrlTestCase(unittest.TestCase):
  def runTest(self):
    root_icon = 'root://icons/palette-4.png'
    url = kml.icons.RootIconUrl(root_icon, 192, 32, 32, 32)
    assert 'http://maps.google.com/mapfiles/kml/pal4/icon54.png' == url

    root_icon = 'root://icons/palette-3.png'
    url = kml.icons.RootIconUrl(root_icon, 224, 0, 32, 32)
    assert 'http://maps.google.com/mapfiles/kml/pal3/icon63.png' == url

class ListPaletteTestCase(unittest.TestCase):
  def runTest(self):
    urls2 = kml.icons.ListPalette(2)
    urls3 = kml.icons.ListPalette(3)
    urls4 = kml.icons.ListPalette(4)
    urls5 = kml.icons.ListPalette(5)
    assert 'http://maps.google.com/mapfiles/kml/pal2/icon0.png' == urls2[0]
    for urls in [urls2, urls3, urls4, urls5]:
      want_pal_num = 0
      for url in urls:
        (path,ext) = os.path.splitext(url)
        name = os.path.basename(path)
        got_pal_num = int(name[4:]) # 'icon' is 4 chars
        assert want_pal_num == got_pal_num
        want_pal_num += 1

def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicRootIconUrlTestCase())
  suite.addTest(ListPaletteTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

