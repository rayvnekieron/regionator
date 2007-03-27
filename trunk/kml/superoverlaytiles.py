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
import kml.superoverlay

class SuperOverlayTileRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self, superoverlay ,exor):
    self.__tile_list = superoverlay.TileList()
    self.__dir = superoverlay.OutputDir()
    self.__fmt = superoverlay.OutputImageFormat()
    self.__exor = exor
    self.__verbose = superoverlay.Verbose()

  def _Extract(self,region,tile):

    (fx,fy,fw,fh) = tile.Info()
    obase = os.path.join(self.__dir,repr(region.Id()))

    if self.__verbose:
      print '%d/%d' % (region.Id(),len(self.__tile_list)),'%s.%s'%(obase,self.__fmt)
    
    # XXX resample original image...
    x = int(fx)
    y = int(fy)
    w = int(fw)
    h = int(fh)
    self.__exor.Extract(x,y,w,h,obase)

  def Start(self,region):
    if self.__tile_list.has_key(region.Qid()):
      self._Extract(region,self.__tile_list[region.Qid()])
      return [True,True]
    return [False,False]


def ChopSuperOverlayTiles(superoverlay):

    imgfile = superoverlay.InputImageFile()
    wid = ht = superoverlay.TileSize()
    fmt = superoverlay.OutputImageFormat()
    exor = kml.extractor.Extractor(imgfile,wid,ht,fmt)
    tilehandler = SuperOverlayTileRegionHandler(superoverlay,exor)
    rtor = kml.regionator.Regionator()
    rtor.SetRegionHandler(tilehandler)
    rtor.SetVerbose(superoverlay.Verbose())
    # Descend down from root region extracting the tile for each region
    rtor.Regionate(superoverlay.RootRegion())
    
    return rtor

