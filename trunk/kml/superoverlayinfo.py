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


""" class SuperOverlayInfo

Phase 1 of SuperOverlay creation

Build the set of regions that include pixels from
the image and the tile offsets for each region.

"""

import kml.regionator
import kml.latlon
import kml.qidboxes
import kml.genkml
import kml.tile
import kml.image
import kml.superoverlay

class SuperOverlayInfoRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self, superoverlay):
    self.__image = superoverlay.Image()
    self.__twid = superoverlay.TileSize()
    self.__tht = superoverlay.TileSize()
    self.__maxdepth = 0
    self.__count = 0
    self.__tiles = {}

  def Start(self,region):
    # Are there any pixels in this region?
    # If so get the offsets and tile dimensions
    (n,s,e,w) = region.NSEW()
    if self.__image.HasPixels(n,s,e,w):
      self.__count += 1
      rd = region.Depth()
      if rd > self.__maxdepth:
        self.__maxdepth = rd
      tile = self.__image.Tile(n,s,e,w)
      self.__tiles[region.Qid()] = tile
      if tile.Wid() > self.__twid * 2 or tile.Ht() > self.__tht * 2:
        return [True,True]
      return [True,False]
    return [False,False]

  def MaxDepth(self):
    return self.__maxdepth

  def RegionCount(self):
    return self.__count

  def Tiles(self):
    return self.__tiles


"""
class SuperOverlayInfo:

  def __init__(self, superoverlay):
    self.__superoverlay = superoverlay
    self.__infohandler = SuperOverlayInfoRegionHandler(superoverlay)
    self.__rtor = kml.regionator.Regionator()
    self.__rtor.SetRegionHandler(self.__infohandler)

  def Regionate(self):

    # Descend down from this node finding
    # the tile for each region at each
    # level of hierarchy down to the specified tile size
    self.__rtor.Regionate(self.__superoverlay.RootRegion())

    self.__superoverlay.SetTileList(self.__infohandler.Tiles())
    
    return self.__rtor
"""

def FindSuperOverlayTiles(superoverlay):
    infohandler = SuperOverlayInfoRegionHandler(superoverlay)
    rtor = kml.regionator.Regionator()
    rtor.SetRegionHandler(infohandler)
    rtor.SetVerbose(superoverlay.Verbose())
    rtor.Regionate(superoverlay.RootRegion())
    return infohandler.Tiles()
