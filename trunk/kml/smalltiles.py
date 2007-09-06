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

import math
import os
import kml.coordbox
import kml.feature
import kml.genkml
import kml.genxml
import kml.kmlparse
import kml.kmz
import kml.regionator
import kml.walk

def TileKey(n,s,e,w):
  return '%s+%s+%s+%s' % (n,s,e,w)

def FindRegion(feature_node):
  region_node = kml.kmlparse.GetFirstChildElement(feature_node, 'Region')
  if region_node:
    return region_node
  # We didn't have our own Region so walk up the Container hierarchy
  if kml.feature.IsContainer(feature_node.parentNode):
    return FindRegion(feature_node.parentNode)
  return None

def CreateHtmlAnchor(lon,lat,href):
  return '<a href="%s">%f,%f</a><br/>' % (href,lon,lat)

def WriteHtmlFile(html_line_list, output):
  f = open(output, 'w')
  f.write("\n".join(html_line_list).encode('utf-8'))
  f.close()

class TileNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self):
    self.__kml_doc = kml.genxml.Document()
    self.__shortest = 180
    self.__tallest = 0
    
    self.__tilemap = {}
    self.__boxes = []
    self.__count = 0

  def HandleNode(self, href, node, llab, lod):
    print href.Href()
    # A given KML file can have multiple GroundOverlays
    go_nodelist = node.getElementsByTagName('GroundOverlay')
    for go_node in go_nodelist:
      # Could use the GO's LatLonBox, but Region is slightly safer.
      region_node = FindRegion(go_node)
      if not region_node:
        continue
        
      (llab, lod) = kml.kmlparse.ParseRegion(region_node)

      # Skip bad regions
      if not (llab.north and llab.south and llab.east and llab.west):
        continue

      # Avoid dups
      tile_key = TileKey(llab.north,llab.south,llab.east,llab.west)
      if self.__tilemap.has_key(tile_key):
        continue

      icon_node = kml.kmlparse.GetFirstChildElement(go_node, 'Icon')
      go_href = kml.kmlparse.GetSimpleElementText(icon_node, 'href')
      abs_url = kml.href.ComputeChildUrl(href.Href(), go_href)
      print abs_url
      self.__tilemap[tile_key] = abs_url
   
      n = float(llab.north)
      s = float(llab.south)
      e = float(llab.east)
      w = float(llab.west)
      ht = n - s
      print self.__count, ht
      if ht < self.__shortest:
        self.__shortest = ht
      if ht > self.__tallest:
        self.__tallest = ht
      self.__boxes.append((n,s,e,w))
      self.__count += 1

  def WriteFile(self, level, name, output):
    height = self.__shortest * ((level+1) ** 2)
    # Make it a range...
    max_height = height * 1.5
    min_height = height * .8
    print 'Found %d regions' % len(self.__boxes)
    print 'Shortest %f, tallest %f' % (self.__shortest, self.__tallest)
    depth = math.log(self.__tallest/self.__shortest, 2)
    print 'Depth (guess) %d' % depth
    num = 0
    html = []
    html.append('<html>')
    html.append('<body>')
    for (n,s,e,w) in self.__boxes:
      ht = n - s 
      # print num, ht
      if ht < max_height and ht > min_height:
        tile_key = TileKey(repr(n), repr(s), repr(e), repr(w))
        (lon,lat) = kml.coordbox.MidPoint(n,s,e,w)
        html.append(CreateHtmlAnchor(lon,lat,self.__tilemap[tile_key]))
        print lon,lat,self.__tilemap[tile_key]
        num += 1
    html.append('</body>')
    html.append('</html>')
    WriteHtmlFile(html, output)


def FindTiles(inputkml, level, name, output):
  tile_node_handler = TileNodeHandler()
  hierarchy = kml.walk.KMLHierarchy()
  hierarchy.SetNodeHandler(tile_node_handler)
  hierarchy.Walk(inputkml, None, None)
  tile_node_handler.WriteFile(level, name, output)

