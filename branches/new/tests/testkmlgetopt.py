#!/usr/bin/env python

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

import unittest

import kml.kmlgetopt

class BasicGetoptTestCase(unittest.TestCase):
  def runTest(self):
    argv = '-a -b hi'.split(' ')
    go = kml.kmlgetopt.Getopt(argv, 'ab:')
    assert True == go.Get('a')
    assert 'hi' == go.Get('b')
    assert False == go.Get('z')

def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicGetoptTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())
