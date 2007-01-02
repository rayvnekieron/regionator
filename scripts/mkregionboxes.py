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

"""

Generate Region LineString boxes for each Region in the KML hierarchy

"""


import sys
import kml.kmlparse
import kml.genxml
import kml.genkml
import kml.walk


if len(sys.argv) != 3:
  print 'usage: %s input.kml boxes.kml' % sys.argv[0]
  sys.exit(1)

inputkml = sys.argv[1]
outputkml = sys.argv[2]


class RegionBoxNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self):
    self.__kml_doc = kml.genxml.Document()

  def HandleNode(self, href, node, llab, lod):
    region_nodelist = node.getElementsByTagName('Region')
    for region in region_nodelist:
      (llab_node, lod_node) = kml.kmlparse.ParseRegion(region)
      llab = kml.kmlparse.ParseLatLonAltBox(llab_node)
      lod = kml.kmlparse.ParseLod(lod_node)
      region_box = kml.genkml.RegionBox('x',
                                        float(llab.north),
                                        float(llab.south),
                                        float(llab.east),
                                        float(llab.west),
                                        float(lod.minLodPixels),
                                        float(lod.maxLodPixels))
      self.__kml_doc.Add_Feature(region_box)

  def WriteFile(self, kmlfile):
    k = kml.genxml.Kml()
    k.Feature = self.__kml_doc.xml()
    f = open(kmlfile, 'w')
    f.write(k.xml())
    f.close()


region_box_node_handler = RegionBoxNodeHandler()
hierarchy = kml.walk.KMLHierarchy()
hierarchy.SetNodeHandler(region_box_node_handler)
hierarchy.Walk(inputkml, None, None)
region_box_node_handler.WriteFile(outputkml)


