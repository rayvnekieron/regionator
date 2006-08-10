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


""" class SuperOverlayKML

Phase 2 of SuperOverlay creation.

Generate KML based on Tile list generated in phase 1

"""

import kml.regionator
import kml.latlon
import kml.genkml
import kml.tile

class SuperOverlayKMLRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self,tiles,maxdepth,fmt,base_draworder):
    self.__tiles = tiles
    self.__maxdepth = maxdepth
    self.__fmt = fmt
    self.__base_draworder = base_draworder

  def Start(self,region):
    if self.__tiles.has_key(region.Qid()):
      return [True,True]
    return [False,False]

  # sets NetworkLink Region lods...
  # which should always be max=-1
  # regionData sets Region for the KML objects
  def PixelLod(self,region):
    return (128,-1)

  def Data(self,region):
    # This is safe because Start() found this key
    tile = self.__tiles[region.Qid()]

    # Note: tile's llbox _may_ be smaller than
    # the Region.  Region used purely for LOD purposes...
    (n,s,e,w) = tile.NSEW()
    href = '%s.%s' % (region.Id(),self.__fmt)
    draworder = self.__base_draworder + region.Depth()

    return kml.genkml.GroundOverlay(n,s,e,w,href,draworder)


class SuperOverlayKML:

  # 1) create/init
  def __init__(self,rootregion,tiles,maxdepth,fmt,base_draworder,dir):
    self.__rootregion = rootregion
    self.__kmlhandler = SuperOverlayKMLRegionHandler(tiles,maxdepth,fmt,base_draworder)
    print 'SUPEROVERLAYKML.__init__()'
    self.__rtor = kml.regionator.Regionator()
    self.__rtor.SetRegionHandler(self.__kmlhandler)
    self.__rtor.SetOutputDir(dir)

  # 2) regionate
  def Regionate(self):

    # Descend down from root region node creating a KML file # for each tile
    self.__rtor.Regionate(self.__rootregion)
    
    return self.__rtor

