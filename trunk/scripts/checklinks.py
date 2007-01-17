#!/usr/bin/python

# Check all link targets in a KML file/hierarchy.

import sys
import kml.walk

if len(sys.argv) != 2:
  print 'usage: %s url.kml' % sys.argv[0]
  sys.exit(1)

inputkml = sys.argv[1]

class HrefNodeHandler(kml.walk.KMLNodeHandler):
  def HandleNode(self, href, node, llab, lod):
    parent = href.Href()
    print 'P  ',parent
    href_nodelist = node.getElementsByTagName('href')
    for href_node in href_nodelist:
      child =  kml.kmlparse.GetText(href_node)
      print 'C  ',child
      url = kml.href.ComputeChildUrl(parent, child)
      print 'U  ',url
      data = kml.href.FetchUrl(url)
      if data:
        print 'D  ',len(data)
      else:
        print 'ERR',child


hier = kml.walk.KMLHierarchy()
hier.SetNodeHandler(HrefNodeHandler())
hier.Walk(inputkml)
 
