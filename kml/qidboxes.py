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

""" MakeQidBoxes()

Builds a single flat KML file of one Placemark LineString
with the Region for each qid in the given regionator's qid list.
Use on a kml.regionator.Regionator()-derived class after Regionate().

Principally for debugging purposes: permits a tour of a given
dataset's Regions.

"""

import kml.regionator
import kml.genxml
import kml.genkml
import kml.kmlparse
import kml.walk


def MakeQidBoxes(rtor,boxfile):

  """
  Creates a single KML document of Region boxes (LineStrings).

  Args:
    boxfile: file to write the KML document
  """

  document = kml.genxml.Document()
  
  rootregion = rtor.RootRegion()

  qids = rtor.QidList()
  for qid in qids:
    r = rootregion.Region(qid)
    (n,s,e,w) = r.NSEW()
    (minpx,maxpx) = rtor.LodPixels(r)
    name = 'qid %s' % qid
    document.Add_Feature(kml.genkml.RegionBox(name,n,s,e,w,minpx,maxpx))

  k = kml.genxml.Kml()
  k.Feature = document.xml()

  f = open(boxfile,'w')
  f.write(k.xml())
  f.close()



class RegionBoxNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self):
    self.__kml_doc = kml.genxml.Document()

  def HandleNode(self, href, node, llab, lod):
    region_nodelist = node.getElementsByTagName('Region')
    for region in region_nodelist:
      (llab, lod) = kml.kmlparse.ParseRegion(region)
      if not (llab.north and llab.south and llab.east and llab.west):
        continue
      if not lod.minLodPixels:
        lod.minLodPixels = 0
      if not lod.maxLodPixels:
        lod.maxLodPixels = -1
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
    f.write(k.xml().encode('utf-8'))
    f.close()


def MakeRegionBoxes(inputkml, outputkml):

  """Make a KML file of a LineString box for each region in the input hierarchy

  Args:
    inputkml: KML/KMZ file with Regions and/or NetworkLinks
    outputkml: KML file of one Region LineString for each region in the input
  """

  region_box_node_handler = RegionBoxNodeHandler()
  hierarchy = kml.walk.KMLHierarchy()
  hierarchy.SetNodeHandler(region_box_node_handler)
  hierarchy.Walk(inputkml, None, None)
  region_box_node_handler.WriteFile(outputkml)

