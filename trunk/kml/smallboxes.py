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
$URL: https://regionator.googlecode.com/svn/trunk/kml/qidboxes.py $
$Revision: 317 $
$Date: 2007-04-30 19:43:02 -0700 (Mon, 30 Apr 2007) $
"""

import kml.regionator
import kml.genxml
import kml.genkml
import kml.kmlparse
import kml.walk

class SmallBoxNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self):
    self.__kml_doc = kml.genxml.Document()
    self.__smallest = 180
    self.__boxes = []
    self.__count = 0

  def HandleNode(self, href, node, llab, lod):
    region_nodelist = node.getElementsByTagName('Region')
    for region in region_nodelist:
      (llab, lod) = kml.kmlparse.ParseRegion(region)
      if not (llab.north and llab.south and llab.east and llab.west):
        continue
      n = float(llab.north)
      s = float(llab.south)
      e = float(llab.east)
      w = float(llab.west)
      ht = n - s
      print self.__count, ht
      if ht < self.__smallest:
        self.__smallest = ht
      self.__boxes.append((n,s,e,w))
      self.__count += 1

  def WriteFiles(self, outputdir):
    print 'total boxes',len(self.__boxes)
    count = 0
    for (n,s,e,w) in self.__boxes:
      ht = n - s 
      print count, ht
      if ht > self.__smallest:
        continue
      WriteKmlBoxFile(n, s, e, w, count, outputdir)
      count += 1

def WriteKmlBoxFile(n,s,e,w,num,dir):
  k = kml.genxml.Kml()
  k.Feature = kml.genkml.Box(n,s,e,w,num)
  kmlfile = os.path.join(dir,num,'.kml')
  print kmlfile
  f = open(kmlfile, 'w')
  f.write(k.xml().encode('utf-8'))
  f.close()


def MakeSmallBoxes(inputkml, outputdir):

  """Make a KML file of a LineString box for each region in the input hierarchy

  Args:
    inputkml: KML/KMZ file with Regions and/or NetworkLinks
    outputkml: KML file of one Region LineString for each region in the input
  """

  small_box_node_handler = SmallBoxNodeHandler()
  hierarchy = kml.walk.KMLHierarchy()
  hierarchy.SetNodeHandler(small_box_node_handler)
  hierarchy.Walk(inputkml, None, None)
  os.makedirs(outputdir)
  small_box_node_handler.WriteFiles(outputdir)

