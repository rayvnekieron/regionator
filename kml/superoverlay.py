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


import getopt
import sys
import os

import kml.image
import kml.superoverlayinfo
import kml.superoverlaykml
import kml.superoverlaytiles
import kml.tile
import kml.version
import kml.kmlparse
import kml.region


class SuperOverlayConfig(object):

  def __init__(self, args):
    self.__image = None
    self.__image_file = None
    self.__tile_size = 256
    self.__base_draw_order = 0
    self.__time_span = None
    self.__altitude = 0
    self.__gokml = None
    self.__verbose = False
    self.__tiles = {}
    self.__root_kml = False
    self.__output_dir = False

    self._GetOpt(args)

    if not self.__image_file:
      raise "image file required"
    if not self.__output_dir:
      raise "output dir required"

    self._InitImage()

  def _GetOpt(self, args):
    (opts, left_over_args) = getopt.getopt(args, "i:k:r:d:t:v")
    for (option, value) in opts:
      if option == '-i':
        self.__image_file = value
      elif option == '-k':
        self.__gokml = value
      elif option == '-r':
        self.__root_kml = value
      elif option == '-d':
        self.__output_dir = value
      elif option == '-t':
        self.__tile_size = int(value)
      elif option == '-v':
        self.__verbose = True

  def _InitImage(self):
    self.__image = kml.image.Image(self.__image_file)

    if self.__gokml:
      self._ParseGoFile(self.__gokml)

    if not self.__image.ValidNSEW():
      (n,s,e,w) = self.__image.NSEW()
      raise "invalid image bounding box" # XXX


  def _ParseGoFile(self, gokml):
    kp = kml.kmlparse.KMLParse(gokml)

    # if there's a LatLonBox use it
    latlonbox = kp.ExtractLatLonBox()
    if latlonbox:
      n = float(latlonbox.north)
      s = float(latlonbox.south)
      e = float(latlonbox.east)
      w = float(latlonbox.west)
      self.__image.SetNSEW(n, s, e, w)

    groundoverlay = kp.ExtractGroundOverlay()
    if groundoverlay.drawOrder:
      self.__base_draw_order = int(groundoverlay.drawOrder)
    if groundoverlay.altitude and groundoverlay.altitudeMode == 'absolute':
      self.__altitude = int(groundoverlay.altitude)

    timespan = kp.ExtractTimeSpan()
    if timespan:
      self.__time_span = timespan.xml()

  def SetImageFile(self, image_file):
    self.__image_file = image_file
    self._InitImage()

  def Image(self):
    return self.__image

  def TileSize(self):
    return self.__tile_size

  def RootRegion(self):
    if self.__image:
       (n,s,e,w) = self.__image.NSEW()
       return kml.region.RootSnap(n,s,e,w)
    return None

  def TimePrimitive(self):
    return self.__time_span

  def Altitude(self):
    return self.__altitude

  def SetTileList(self, tiles):
    self.__tiles = tiles

  def TileList(self):
    return self.__tiles

  def OutputImageFormat(self):
    if self.__image:
      return self.__image.OutputFormat()
    return None

  def BaseDrawOrder(self):
    return self.__base_draw_order

  def InputImageFile(self):
    return self.__image_file

  def OutputDir(self):
    return self.__output_dir

  def RootKml(self):
    return self.__root_kml

  def Verbose(self):
    return self.__verbose


def CreateSuperOverlay(superoverlay):

  """This creates a SuperOverlay.

  A SuperOverlay is a Region-based NetworkLink hierarchy of KML GroundOverlays
  from the given image at the specified location.  The image file is
  not altered.

  If the input image is a north-up EPSG:4326 (WGS 84) geotiff
  the image bounding box (north, south, east, west edges) is
  taken from the geotiff tags.  If bounding box arguments are
  supplied the geotiff tags are not used.

  If the input image is not a geotiff the image bounding box
  must be supplied.

  If a KML file with a GroundOverlay is defined the values found there
  for LatLonBox north, south, east, and west, and/or TimeSpan begin,end,
  and/or GroundOverlay drawOrder, altitude, altitudeMode are used
  in creation of the SuperOverlay.  The Icon/href is ignored and as such
  this GroundOverlay KML file can be used for planning purpose likely
  with a downsampled version of the image.

  Note that the drawOrder is the drawOrder of the coarsest tile and that
  each level of finer detail is drawn with a higher drawOrder.  To specify
  an overall drawOrder of multiple SuperOverlays the "base" drawOrder of each
  must be properly spaced for best results.  A very large SuperOverlay can
  use 20+ levels of imagery.
 
  The specified output directory must not already exist.
  All links between KML and image tiles within this directory
  are relative such that the directory can be used either
  locally or copied to the appropriate http-serving directory
  for access via a http-based NetworkLink root file.

  The root file is a small NetworkLink KML file which points
  to the top of the SuperOverlay.  The href to 1.kml should be
  changed to be the URL of the directory.  This file is
  distributed to users of the SuperOverlay.  Note that the
  NetworkLink within is a Region-based load and that opening
  this file in Google Earth neither loads any imagery nor
  flies to the SuperOverlay.  When the user flies to the
  vicinity of the SuperOverlay this first NetworkLink is loaded
  which triggers further NetworkLink loads within the SuperOverlay
  as appropriate for the users viewpoint.

  A KML file of one LineString box per image tile in the
  created image hierachy is saved to dir/qidboxes.kml.  This is
  created for debugging and illustration purposes and is not
  required for proper functioning of the SuperOverlay.
  Note that a LineString does not exactly follow a longitude line.

  Error handling is not graceful: partial output data is not removed.
  and error messages may come in the form of a Python exception dump.

  Args:
    superoverlay: kml.superoverlay.SuperOverlayConfig()

  Returns:
    bool: True on complete success, False on any failure
  """



  # Phase 1 - find the regions with tiles
  
  tile_list = kml.superoverlayinfo.FindSuperOverlayTiles(superoverlay)
  superoverlay.SetTileList(tile_list)
  
  # Phase 2 - generate the KML

  os.makedirs(superoverlay.OutputDir())
  
  rtor = kml.superoverlaykml.CreateSuperOverlayKML(superoverlay)
  
  # debug linestring boxes
  
  qidboxes = os.path.join(superoverlay.OutputDir(), 'qidboxes.kml')
  kml.qidboxes.MakeQidBoxes(rtor, qidboxes)
  
  if superoverlay.RootKml():
    kml.regionator.MakeRootKML(superoverlay.RootKml(),
                               superoverlay.RootRegion(),
                               128,
                               superoverlay.OutputDir())

  # Phase 3 - chop out image tiles
  
  kml.superoverlaytiles.ChopSuperOverlayTiles(superoverlay)
  return True


def SuperOverlay(imagefile, root, dir, gofile=None):

  """DEPRECATED: Use CreateSuperOverlay()"""

  print 'version',kml.version.Revision()

  argv = []
  argv.append('-i')
  argv.append(imagefile)
  argv.append('-k')
  argv.append(gofile)
  argv.append('-r')
  argv.append(root)
  argv.append('-d')
  argv.append(dir)
  argv.append('-v')
  try:
    status = CreateSuperOverlay(SuperOverlayConfig(argv))
  except:
    return False
