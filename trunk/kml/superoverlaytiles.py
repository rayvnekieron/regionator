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

""" class SuperOverlayTiles

Phase 3 of SuperOverlay creation.

Extract tiles from image based on Tile list generated in phase 1

Handy to keep this separate from KML generation.

"""

import os

import kml.regionator
import kml.latlon
import kml.genkml
import kml.tile
import kml.extractor

class SuperOverlayTileRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self,tiles,dir,fmt,exor):
    self.__tiles = tiles
    self.__dir = dir
    self.__fmt = fmt
    self.__exor = exor

  def _Extract(self,region,tile):

    (fx,fy,fw,fh) = tile.Info()
    obase = os.path.join(self.__dir,repr(region.Id()))

    print '%d/%d' % (region.Id(),len(self.__tiles)),'%s.%s'%(obase,self.__fmt)
    
    # XXX resample original image...
    x = int(fx)
    y = int(fy)
    w = int(fw)
    h = int(fh)
    self.__exor.Extract(x,y,w,h,obase)

  def Start(self,region):
    if self.__tiles.has_key(region.Qid()):
      self._Extract(region,self.__tiles[region.Qid()])
      return [True,True]
    return [False,False]


class SuperOverlayTiles:

  # 1) create/init

  def __init__(self,rootregion,tiles,imgfile,dir,fmt,wid,ht):
    exor = kml.extractor.Extractor(imgfile,wid,ht,fmt)
    self.__rootregion = rootregion
    self.__tilehandler = SuperOverlayTileRegionHandler(tiles,dir,fmt,exor)
    self.__rtor = kml.regionator.Regionator()
    self.__rtor.SetRegionHandler(self.__tilehandler)

  # 2) regionate
  def Regionate(self):

    # Descend down from root region extracting the tile for each region
    self.__rtor.Regionate(self.__rootregion)
    
    return self.__rtor

