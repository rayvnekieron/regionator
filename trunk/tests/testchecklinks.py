#!/usr/bin/python

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
import os
import tempfile
import kml.checklinks
import kml.kmlregionator

class NullTestCase(unittest.TestCase):
  def runTest(self):
    # Create an instance with no arguments
    link_checker = kml.checklinks.LinkCheckingNodeHandler('')
    # Do nothing and status should be 0
    assert 0 == link_checker.Status()

class BasicTestCase(unittest.TestCase):
  def setUp(self):
    # Create a Region-based NetworkLink hierarchy to check
    inputkml = 'placemarks.kml'
    minpx = 256
    maxper = 4
    (fd,self.rootkml) = tempfile.mkstemp()
    os.close(fd)
    self.dir = tempfile.mkdtemp()
    verbose = False
    self.rtor = kml.kmlregionator.RegionateKML(inputkml,
                                               minpx,
                                               maxper,
                                               self.rootkml,
                                               self.dir,
                                               verbose)

  def tearDown(self):
    os.unlink(self.rootkml)
    for file in os.listdir(self.dir):
      os.unlink(os.path.join(self.dir, file))
    os.rmdir(self.dir)

  def testCheckLinksOnRelativeKml(self):
    # MakeRootKML basically expects a relative dir but we hand it
    # an absolute path in setUp.  So we hop over it here.
    kml1 = os.path.join(self.dir, '1.kml')
    status = kml.checklinks.CheckLinks(['-k','-r'], kml1)
    assert 0 == status

  def CheckLinks(self):
    link_checker = kml.checklinks.LinkCheckingNodeHandler(['-k','-r','-s'])
    hier = kml.walk.KMLHierarchy()
    hier.SetNodeHandler(link_checker)
    hier.Walk(os.path.join(self.dir, '1.kml'))
    return link_checker.Statistics()

  def testLinkCheckerOnRelativeKml(self):
    (nodes, kmls, htmls, rel, abs, hn, empty, errs, md5) = self.CheckLinks()
    assert 50 == nodes
    assert 49 == kmls
    assert 0 == htmls
    assert 49 == rel
    assert 0 == abs
    assert 0 == hn
    assert 0 == empty
    assert 0 == errs
    # Can't assert much more due to the version number in the generated kml.
    assert md5

  def testLinkCheckerOnDamagedKml(self):
    before = self.CheckLinks()
    os.unlink(os.path.join(self.dir, '6.kml'))
    after = self.CheckLinks()
    # 6.kml was a leaf node, so the after check finds one less node
    assert 50 ==  before[0]
    assert 49 == after[0]
    # checksum is different
    assert before[8] != after[8]

class BasicHtmlTestCase(unittest.TestCase):
  def runTest(self):
    link_checker = kml.checklinks.LinkCheckingNodeHandler(['-h','-r','-k','-s'])
    hier = kml.walk.KMLHierarchy()
    hier.SetNodeHandler(link_checker)
    hier.Walk('html.kml')
    (nodes, kmls, htmls, rel, abs, hn, empty, errs, md5) = \
                                                      link_checker.Statistics()
    # The file html.kml is the one and only KML in the hierarchy:
    assert 1 == nodes
    # There is one href in KML (IconStyle/Icon/href):
    assert 1 == kmls
    # There are 8 hrefs in the HTML:
    assert 8 == htmls
    # One hrefs are relative:
    assert 3 == rel
    # Checking of absolute links not requested:
    assert 0 == abs
    # No hostname-only hrefs:
    assert 0 == hn
    # One href is empty:
    assert 1 == empty
    # Three errors due to non-existent files:
    assert 3 == errs
    # Yes, there's a checksum
    assert md5

class BadEncodingTestCase(unittest.TestCase):
  def setUp(self):
    self.link_checker = kml.checklinks.LinkCheckingNodeHandler(['-h','-r','-k'])
    self.hier = kml.walk.KMLHierarchy()
    self.hier.SetNodeHandler(self.link_checker)

  def testCorrectEncoding(self):
    self.hier.Walk('es-latin1.kml')
    (nodes, kmls, htmls, rel, abs, hn, empty, errs, md5) = \
                                                 self.link_checker.Statistics()
    assert 1 == nodes
    assert 1 == kmls
    assert 8 == htmls
    assert 3 == rel
    # Not checking absolute links (no '-a' specified):
    assert 0 == abs
    # "www.google.fr":
    assert 1 == hn
    assert 0 == empty
    # None of the relative links exist here:
    assert 3 == errs
    assert None == md5

  def testWrongEncoding(self):
    status = self.hier.Walk('es-utf1.kml')
    # xml.dom.minidom will fail to parse, hence no nodes, no nothin':
    assert status == False
    (nodes, kmls, htmls, rel, abs, hn, empty, errs, md5) = \
                                                 self.link_checker.Statistics()
    assert 0 == nodes
    assert 0 == kmls
    assert 0 == htmls
    assert 0 == rel
    assert 0 == abs
    assert 0 == hn
    assert 0 == empty
    assert 0 == errs
    assert None == md5

class NonExistentRootTestCase(unittest.TestCase):
  def runTest(self):
    status = kml.checklinks.CheckLinks('','this-file-does-not-exist')
    assert -1 == status
 

def suite():
  suite = unittest.TestSuite()
  suite.addTest(NullTestCase())
  suite.addTest(BasicTestCase("testCheckLinksOnRelativeKml"))
  suite.addTest(BasicTestCase("testLinkCheckerOnRelativeKml"))
  suite.addTest(BasicTestCase("testLinkCheckerOnDamagedKml"))
  suite.addTest(BasicHtmlTestCase())
  suite.addTest(BadEncodingTestCase("testWrongEncoding"))
  suite.addTest(BadEncodingTestCase("testCorrectEncoding"))
  suite.addTest(NonExistentRootTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

