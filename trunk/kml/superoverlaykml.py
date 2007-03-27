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
import kml.superoverlay

class SuperOverlayKMLRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self, superoverlay):
    self.__tile_list = superoverlay.TileList()
    self.__fmt = superoverlay.OutputImageFormat()
    self.__tile_size = superoverlay.TileSize()
    self.__base_draw_order = superoverlay.BaseDrawOrder()
    self.__altitude = None
    self.__altitudeMode = None

  def SetAltitude(self, altitude):
    self.__altitude = altitude
    self.__altitudeMode = 'absolute'

  def Start(self,region):
    if self.__tile_list.has_key(region.Qid()):
      return [True,True]
    return [False,False]

  # sets NetworkLink Region lods...
  # which should always be max=-1
  # regionData sets Region for the KML objects
  def PixelLod(self,region):
    min_lod_pixels = self.__tile_size/2
    return (min_lod_pixels,-1)

  def Data(self,region):
    # This is safe because Start() found this key
    tile = self.__tile_list[region.Qid()]

    # Note: tile's llbox _may_ be smaller than
    # the Region.  Region used purely for LOD purposes...
    (n,s,e,w) = tile.NSEW()
    href = '%s.%s' % (region.Id(),self.__fmt)
    draworder = self.__base_draw_order + region.Depth()

    groundoverlay = kml.genxml.GroundOverlay()

    latlonboxkml = kml.genkml.LatLonBox(n,s,e,w)
    groundoverlay.LatLonBox = latlonboxkml

    icon = kml.genxml.Icon()
    icon.href = href
    groundoverlay.Icon = icon.xml()

    groundoverlay.drawOrder = draworder

    if self.__altitude:
      groundoverlay.altitude = self.__altitude

    if self.__altitudeMode:
      groundoverlay.altitudeMode = self.__altitudeMode

    return groundoverlay.xml()


def CreateSuperOverlayKML(superoverlay):

    kmlhandler = SuperOverlayKMLRegionHandler(superoverlay)
    rtor = kml.regionator.Regionator()
    rtor.SetRegionHandler(kmlhandler)
    rtor.SetOutputDir(superoverlay.OutputDir())

    timeprimitive = superoverlay.TimePrimitive()
    if timeprimitive:
      rtor.SetTimePrimitive(timeprimitive)

    altitude = superoverlay.Altitude()
    if altitude:

      # for Region LatLonAltBox minAltitude/maxAltitude/altitudeMode
      # Region for GroundOverlays: minAltitude = maxAltitude = altitude
      rtor.SetAltitude(altitude, altitude)

      # for GroundOverlay altitude/altitudeMode
      kmlhandler.SetAltitude(altitude)

    rtor.SetVerbose(superoverlay.Verbose())
    # Descend down from root region node creating a KML file # for each tile
    rtor.Regionate(superoverlay.RootRegion())
    
    return rtor
