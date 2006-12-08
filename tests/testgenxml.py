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
import kml.genxml


class BasicSimpleElementTestCase(unittest.TestCase):
  def runTest(self):
    xml = kml.genxml.SimpleElement('mytag','mycontent')
    assert xml == '<mytag>mycontent</mytag>\n', 'mytag SimpleElement failed'


class BasicSimpleElementListTestCase(unittest.TestCase):
  def runTest(self):
    nvp_list = [['a','0'],['b','1'],['c','2']]
    xml = kml.genxml.SimpleElementList(nvp_list)
    assert xml == '<a>0</a>\n<b>1</b>\n<c>2</c>\n', 'abc element list failed'


class BasicElementAttributesTestCase(unittest.TestCase):
  def runTest(self):
    nvp_list = [['a','0'],['b','1'],['c','2']]
    attrs = kml.genxml.ElementAttributes(nvp_list)
    assert attrs == ' a="0" b="1" c="2"', 'abc attribute list failed'


class EmptyComplexElementTestCase(unittest.TestCase):
  def runTest(self):
    empty = kml.genxml.ComplexElement('empty',None,None,None,None)
    assert empty == '<empty/>\n', 'empty complex element failed'


basic_complex_xml = ['<xyz>\n',
                     '<aa>00</aa>\n',
                     '<bb>11</bb>\n',
                     '<cc>22</cc>\n',
                     '<hi><ho>there</ho></hi>\n',
                     '<bye/>\n',
                     '</xyz>\n']


class BasicComplexElementTestCase(unittest.TestCase):
  def runTest(self):
    elements = [['aa','00'],['bb','11'],['cc','22']]
    children = '<hi><ho>there</ho></hi>\n<bye/>\n'
    xml = kml.genxml.ComplexElement('xyz', None, None, elements, children)
    assert xml == "".join(basic_complex_xml), 'xyz complex element failed'
    

def suite():
  suite = unittest.TestSuite()
  suite.addTest(BasicSimpleElementTestCase())
  suite.addTest(BasicSimpleElementListTestCase())
  suite.addTest(BasicElementAttributesTestCase())
  suite.addTest(EmptyComplexElementTestCase())
  suite.addTest(BasicComplexElementTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())
