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

"""class SuperOverlayPoly

Debug class to visualize image tiles

Show color coded polygons at superoverlay tiles.
Takes the same input as SuperOverlayKML.

"""

import os

import kml.regionator
import kml.latlon
import kml.genkml
import kml.tile

class SuperOverlayPolyRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self,tiles,maxdepth,outfd):
    self.__tiles = tiles
    self.__maxdepth = maxdepth
    self.__outfd = outfd

  def Start(self,region):
    if self.__tiles.has_key(region.Qid()):
      return [True,True]
    return [False,False]

  def PixelLod(self,region):
    # Yes this is the default
    return (128,-1)

  def Data(self,region):
    tile = self.__tiles[region.Qid()]
    depth = region.Depth()

    (n,s,e,w) = tile.NSEW()
    kmlpoly = kml.genkml.PolygonBox(n,s,e,w,0)

    fill = 1
    outline = 1
    a = 127
    color = (depth * 255)/self.__maxdepth
    b = 255 - color
    r = color
    g = 0
    kmlpolystyle = kml.genkml.PolyStyle(a,b,g,r,fill,outline)

    # NOTE!  The region's NSEW maybe be different than the tile...
    (n,s,e,w) = region.NSEW()
    # LOD different than the "feeder" KML LOD set in PixelLod() above
    kmlregion = kml.genkml.RegionLod(n, s, e, w, 128, 1024)

    _kml = []
    _kml.append('<Placemark>\n')
    _kml.append('<name>%s</name>\n' % region.Qid())
    _kml.append(kmlregion)
    _kml.append('<Style>\n')
    _kml.append(kmlpolystyle)
    _kml.append('</Style>\n')
    _kml.append(kmlpoly)
    _kml.append('</Placemark>\n')
    kstr = "".join(_kml)
    self.__outfd.write(kstr)
    return kstr


class SuperOverlayPoly:

  """ class SuperOverlayPoly


  """

  # 1) create/init
  def __init__(self,rootregion,tiles,maxdepth,dir):

    """

    Args:
      rootregion: kml.region.Region
      tiles: list of kml.tiles.Tile
      maxdepth: depth of finest region
      dir: where to save the KML

    """

    self.__rootregion = rootregion
    allinonefile = os.path.join(dir,'polyfile.kml')
    self.__fd = open(allinonefile,'w')
    self.__fd.write(kml.genkml.KML21())
    self.__fd.write('<Document>\n')
    self.__polyhandler = SuperOverlayPolyRegionHandler(tiles,maxdepth,self.__fd)
    self.__rtor = kml.regionator.Regionator()
    self.__rtor.SetOutputDir(dir)
    self.__rtor.SetRegionHandler(self.__polyhandler)

  # 2) regionate
  def Regionate(self):
    """

    Descend down from root region node creating a polygon
    based on the bbox of the Tile's for that Region.

    Returns:
      rtor

    """

    self.__rtor.Regionate(self.__rootregion)

    self.__fd.write('</Document>\n')
    self.__fd.write('</kml>\n')
    self.__fd.close()
    
    return self.__rtor

