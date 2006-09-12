#!/usr/bin/python

import kml.region
import kml.wms
import kml.href


def testhref(region, month):
  wms_host = 'wms.jpl.nasa.gov'
  wms_path = 'wms.cgi'
  wms_queries = ['VERSION=1.1.1', 'REQUEST=GetMap', 'SRS=EPSG:4326',
                'WIDTH=256', 'HEIGHT=256', 'LAYERS=BMNG',
                'TRANSPARENT=TRUE', 'FORMAT=image/png']

  href = kml.href.Href()
  href.SetHostname(wms_host)
  href.SetPath(wms_path)
  for wq in wms_queries:
    href.AddQuery(wq)
  href.AddQueryNameValue('STYLES', month)
  href.AddQuery(kml.wms.WMSBBOX(region))
  hrefstr = href.Href()
  return hrefstr

region = kml.region.Region(20,10,-80,-100,'0')

got = testhref(region, 'Aug')

want = 'http://wms.jpl.nasa.gov/wms.cgi?VERSION=1.1.1&amp;REQUEST=GetMap&amp;SRS=EPSG:4326&amp;WIDTH=256&amp;HEIGHT=256&amp;LAYERS=BMNG&amp;TRANSPARENT=TRUE&amp;FORMAT=image/png&amp;STYLES=Aug&amp;BBOX=-100.000000,10.000000,-80.000000,20.000000'

if got != want:
  print 'kml.href.Href FAILED'
else:
  print 'kml.href.Href okay'
