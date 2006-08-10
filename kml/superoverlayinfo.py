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

class SuperOverlayInfoRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self,image,twid,tht):
    self.__image = image
    self.__twid = twid
    self.__tht = tht
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
      if tile.Wid() > self.__twid or tile.Ht() > self.__tht:
        return [True,True]
      return [True,False]
    return [False,False]

  def MaxDepth(self):
    return self.__maxdepth

  def RegionCount(self):
    return self.__count

  def Tiles(self):
    return self.__tiles


class SuperOverlayInfo:

  def __init__(self,image,twid,tht):
    self.__image = image
    self.__infohandler = SuperOverlayInfoRegionHandler(image,twid,tht)
    self.__rtor = kml.regionator.Regionator()
    self.__rtor.SetRegionHandler(self.__infohandler)
    self.__twid = twid
    self.__tht = tht

  def Regionate(self):
    (n,s,e,w) = self.__image.NSEW()
    r = kml.region.RootSnap(n,s,e,w)
    self.__rootregion = r

    # Descend down from this node finding
    # the tile for each region at each
    # level of hierarchy down to the specified tile size
    self.__rtor.Regionate(r)
    
    return self.__rtor

  # valid only after regionate

  # a dictionary mapping qid to Tile
  def Tiles(self):
    return self.__infohandler.Tiles()

  def RootRegion(self):
    return self.__rootregion


