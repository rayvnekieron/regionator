#!/usr/bin/python

import unittest

import kml.region
import kml.wms
import kml.href


class SimpleTestCase(unittest.TestCase):
  def runTest(self):
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
    href.SetHostname(wms_host)
    href.SetPath(wms_path)
    for wq in wms_queries:
      href.AddQuery(wq)
    href.AddQueryNameValue('STYLES', wms_month)
    region = kml.region.Region(wms_north, wms_south, wms_east, wms_west, '0')
    href.AddQuery(kml.wms.WMSBBOX(region))
    hrefstr = href.Href()
    assert hrefstr == want

def suite():
  suite = unittest.TestSuite()
  suite.addTest(SimpleTestCase())
  return suite

runner = unittest.TextTestRunner()
runner.run(suite())

