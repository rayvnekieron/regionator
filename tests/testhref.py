#!/usr/bin/python

import unittest

import kml.region
import kml.wms
import kml.href


class SimpleTestCase(unittest.TestCase):
  def runTest(self):
    wms_scheme = 'http'
    wms_host = 'wms.jpl.nasa.gov'
    wms_path = 'wms.cgi'
    wms_queries = ['VERSION=1.1.1', 'REQUEST=GetMap', 'SRS=EPSG:4326',
                'WIDTH=256', 'HEIGHT=256', 'LAYERS=BMNG',
                'TRANSPARENT=TRUE', 'FORMAT=image/png']
    wms_month = 'Aug'
    wms_north = 20
    wms_south = 10
    wms_east = -80
    wms_west = -100

    want = 'http://wms.jpl.nasa.gov/wms.cgi?VERSION=1.1.1&amp;REQUEST=GetMap&amp;SRS=EPSG:4326&amp;WIDTH=256&amp;HEIGHT=256&amp;LAYERS=BMNG&amp;TRANSPARENT=TRUE&amp;FORMAT=image/png&amp;STYLES=Aug&amp;BBOX=-100.000000,10.000000,-80.000000,20.000000'

    href = kml.href.Href()
    href.SetScheme(wms_scheme)
    href.SetHostname(wms_host)
    href.SetPath(wms_path)
    for wq in wms_queries:
      href.AddQuery(wq)
    href.AddQueryNameValue('STYLES', wms_month)
    region = kml.region.Region(wms_north, wms_south, wms_east, wms_west, '0')
    href.AddQuery(kml.wms.WMSBBOX(region))
    hrefstr = href.Href()
    assert hrefstr == want,'bad url [%s]' % hrefstr


class HttpTestCase(unittest.TestCase):
  def runTest(self):
    href = kml.href.Href()
    href.SetUrl('http://foo.com/dir/foo/hi.kml')
    href.SetBasename('hello.kml')
    assert href.Href() == 'http://foo.com/dir/foo/hello.kml'

class FileTestCase(unittest.TestCase):
  def runTest(self):
    href = kml.href.Href()
    href.SetUrl('/a/b/d/hi.kml')
    assert href.GetScheme() == None,'scheme not none'

class RelativeFileTestCase(unittest.TestCase):
  def runTest(self):
    href = kml.href.Href()
    href.SetUrl('foo/goo.kml')
    href.SetBasename('bar/baz.kml')
    assert href.Href() == 'foo/bar/baz.kml','relative file bad'

class SplitKmzTestCase(unittest.TestCase):
  def runTest(self):
    parent_path = 'http://foo.com/able/baker/foo.kml'
    link_path = 'charlie.kmz/delta/epsilon.dae'
    href = kml.href.Href()
    href.SetUrl(parent_path)
    (kmz_url, kmz_file) = kml.href.SplitKmzHref(href, link_path)
    assert kmz_url == 'http://foo.com/able/baker/charlie.kmz'
    assert kmz_file == 'delta/epsilon.dae'

class DotDotTestCase(unittest.TestCase):
  def runTest(self):
    parent_path = 'http://foo.com/able/baker/foo.kml'
    dotdot_path = '../charlie/goo.kml'
    want_path = 'http://foo.com/able/charlie/goo.kml'
    href = kml.href.Href()
    href.SetUrl(parent_path)
    href.SetBasename(dotdot_path)
    assert href.Href() == want_path, 'dot dot href failed'

class NoSuchFetchUrlTestCase(unittest.TestCase):
  def runTest(self):
    nada = kml.href.FetchUrl("xxxp://nosuch.host.com/no/such/file")
    assert nada == None, 'FetchUrl of bad url failed'

class NoSuchFetchUrlTempTestCase(unittest.TestCase):
  def runTest(self):
    nada = kml.href.FetchUrlToTempFile("xxxp://nosuch.host.com/no/such/file")
    assert nada == None, 'FetchUrlToTmpeFile of bad url failed'


def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleTestCase())
  suite.addTest(HttpTestCase())
  suite.addTest(FileTestCase())
  suite.addTest(RelativeFileTestCase())
  suite.addTest(SplitKmzTestCase())
  suite.addTest(DotDotTestCase())
  suite.addTest(NoSuchFetchUrlTestCase())
  suite.addTest(NoSuchFetchUrlTempTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

