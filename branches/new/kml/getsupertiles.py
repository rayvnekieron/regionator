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

import math
import os
import tarfile
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


class SuperTileNodeHandler(kml.walk.KMLNodeHandler):

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

      ht = float(llab.north) - float(llab.south)
      print self.__count, ht
      if ht < self.__shortest:
        self.__shortest = ht
      if ht > self.__tallest:
        self.__tallest = ht
      self.__boxes.append((llab.north,llab.south,llab.east,llab.west))
      self.__count += 1

  def WriteTarFile(self, level, tardir, output):
    tar = tarfile.TarFile(name=output, mode='w')
    height = self.__shortest * ((level+1) ** 2)
    # Make it a range...
    max_height = height * 1.5
    min_height = height * .8
    print 'Found %d regions' % len(self.__boxes)
    print 'Shortest %f, tallest %f' % (self.__shortest, self.__tallest)
    depth = math.log(self.__tallest/self.__shortest, 2)
    print 'Depth (guess) %d' % depth
    num = 0
    for (n,s,e,w) in self.__boxes:
      ht = float(n) - float(s)
      # print num, ht
      if ht < max_height and ht > min_height:
        tile_key = TileKey(n,s,e,w)
        # Presumes the URL is a local file!
        filename = self.__tilemap[tile_key]
        # Presumes unique basename!
        tarname = '%s/%s' % (tardir, os.path.basename(filename))
        print 'Saving %s to %s' % (filename, tarname)
        tar.add(filename, arcname=tarname)
        num += 1
    print 'Save %d tiles to %s' % (num, output)
    tar.close()


def GetSuperTiles(inputkml, level, tardir, output):
  tile_node_handler = SuperTileNodeHandler()
  hierarchy = kml.walk.KMLHierarchy()
  hierarchy.SetNodeHandler(tile_node_handler)
  hierarchy.Walk(inputkml, None, None)
  tile_node_handler.WriteTarFile(level, tardir, output)
