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
import kml.resourcemap


class SimpleResourceMapItemTestCase(unittest.TestCase):
  def runTest(self):
    rmi = kml.resourcemap.ResourceMapItem()
    rmi.ParseTexturesTxtLine('<gp><kp><mid>')
    (gp,kp,mid) = rmi.Mapping()
    assert gp == 'gp','bad geom path in ResourceMapItem'
    assert kp == 'kp','bad kmz path in ResourceMapItem'
    assert mid == 'mid','bad mid in ResourceMapItem'


class NoMidResourceMapItemTestCase(unittest.TestCase):
  def runTest(self):
    rmi = kml.resourcemap.ResourceMapItem()
    rmi.ParseTexturesTxtLine('<../goo/hi.jpg> <../koo/bye.jpg>')
    (gp,kp,mid) = rmi.Mapping()
    assert gp == '../goo/hi.jpg','bad geom path in ResourceMapItem'
    assert kp == '../koo/bye.jpg','bad kmz path in ResourceMapItem'
    assert mid == None,'non None mid in non-mid ResourceMapItem'


class ResourceMapTestCase(unittest.TestCase):
  def setUp(self):
    self.__model = kml.model.Model()
    self.__model.Parse('London_house.kmz')
    textures_txt_data = self.__model.ReadFileData('textures.txt')
    self.__rmap = kml.resourcemap.ResourceMap()
    self.__rmap.ParseTexturesTxt(textures_txt_data)
  def testResourceMapSize(self):
    assert self.__rmap.Size() == 3,'ResourceMap.Size() bad'
  def testResourceMapIterator(self):
    m = []
    for rmap_item in self.__rmap:
      m.append(rmap_item.Mapping())
    assert m[0][0] == '../images/Building3.JPG','textures.txt parse failed 0'
    assert m[2][1] == '../images/GAF_Marquis.jpg','textures.txt parse failed 2'
  def testResourceMapLookup(self):
    kp = self.__rmap.GetKmzPath('../images/Building3.JPG')
    assert kp == '../images/Building3.JPG','rmap kmz lookup failed'
    gp = self.__rmap.GetGeomPath('../images/GAF_Marquis.jpg')
    assert gp == '../images/GAF_Marquis.jpg','rmap geom lookup failed'


class TexturesTxtTestCase(unittest.TestCase):
  def setUp(self):
    f = open('textures.txt','r')
    textures_txt_data = f.read()
    f.close()
    self.__rmap = kml.resourcemap.ResourceMap()
    self.__rmap.ParseTexturesTxt(textures_txt_data)
  def testSize(self):
    assert self.__rmap.Size() == 66,'textures txt rmap size bad'
  def testGeomLookup(self):
    gp = ('../geom/north-face-10noCulling.jpg')
    rmi = self.__rmap.LookupByGeomPath(gp)
    (got_gp,got_kp,got_mid) = rmi.Mapping()
    want_kp = '../kmz/north-face-10noCulling.jpg'
    assert got_kp == want_kp, 'geom lookup failed'
  def testKmzLookup(self):
    rmi = self.__rmap.LookupByKmzPath('../kmz/east-face-1_1.jpg')
    (got_gp, got_kp, id) = rmi.Mapping()
    want_gp = '../geom/east-face-1_1.jpg'
    assert got_gp == want_gp,'kmz lookup failed'
  def testLookupAll(self):
    for rmap_item in self.__rmap:
      (gp,kp,mid) = rmap_item.Mapping()
      assert gp == self.__rmap.GetGeomPath(kp),'GetGeomPath() failed'
      assert kp == self.__rmap.GetKmzPath(gp),'GetKmzPath() failed'


class ResourceMapAddTestCase(unittest.TestCase):
  def runTest(self):
    rmap = kml.resourcemap.ResourceMap()
    rmap.AddResourceMapItem('gpath0','kpath0','mid0')
    rmap.AddResourceMapItem('gpath1','kpath1','mid1')
    got_tt = rmap.Serialize()
    want_tt[0] = '<gpath0>  <kpath0> <mid0>'
    want_tt[1] = '<gpath1>  <kpath1> <mid1>'
    assert got_tt == "\n".join(want_tt), 'resource map serialize failed'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleResourceMapItemTestCase())
  suite.addTest(NoMidResourceMapItemTestCase())
  suite.addTest(ResourceMapTestCase("testResourceMapSize"))
  suite.addTest(ResourceMapTestCase("testResourceMapIterator"))
  suite.addTest(ResourceMapTestCase("testResourceMapLookup"))
  suite.addTest(TexturesTxtTestCase("testSize"))
  suite.addTest(TexturesTxtTestCase("testGeomLookup"))
  suite.addTest(TexturesTxtTestCase("testKmzLookup"))
  suite.addTest(TexturesTxtTestCase("testLookupAll"))
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())
