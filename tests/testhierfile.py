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

import kml.hierfile

class Len3TestCase(unittest.TestCase):
  def setUp(self):
    self.__hf3 = kml.hierfile.HierFile(3)
  def testPath(self):
    path = self.__hf3.Path('foobar')
    assert path == 'foo/bar', 'Len3 Path bad'
  def testMedium(self):
    flatname = 'abcdefgh'
    (dir,name) = self.__hf3.HierName(flatname)
    assert dir == 'abc/def/', 'Len3 medium dirname bad'
    assert name == 'gh', 'Len3 medium name bad'
  def testLong(self):
    flatname = '0123456789abcdefghijklmnopqrstuvwzyz'
    (dir,name) = self.__hf3.HierName(flatname)
    assert dir == '012/345/678/9ab/cde/fgh/ijk/lmn/opq/rst/uvw/',\
           'Len3 long dir bad'
    assert name == 'zyz', 'Len3 long name bad'

class Len6TestCase(unittest.TestCase):
  def setUp(self):
    self.__hf6 = kml.hierfile.HierFile(6)
  def testLong(self):
    flatname = 'abcasd4a1ljplj4poijphkq2lpoiu'
    (dir,name) = self.__hf6.HierName(flatname)
    assert dir == 'abcasd/4a1ljp/lj4poi/jphkq2/', 'Len6 dir bad'
    assert name == 'lpoiu', 'Len6 name bad'

class WriteHierFileTestCase(unittest.TestCase):
  def setUp(self):
    """ """
  def testLen2(self):
    data = 'a little data'
    flatname = 'abc123'
    kml.hierfile.WriteHierFile('hiertestdir', flatname, 'foo', 2, data)
    f = open('hiertestdir/ab/c1/23.foo', 'r')
    got_data = f.read()
    assert data == got_data, 'WriteHierFile Len2 failed'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(Len3TestCase("testPath"))
  suite.addTest(Len3TestCase("testMedium"))
  suite.addTest(Len3TestCase("testLong"))
  suite.addTest(Len6TestCase("testLong"))
  suite.addTest(WriteHierFileTestCase("testLen2"))
  return suite


runner = unittest.TextTestRunner()
runner.run(suite())

