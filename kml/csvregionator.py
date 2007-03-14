"""
Copyright (C) 2007 Google Inc.

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

""" BasicCSVRegionHandler

A Regionator of CSV input data.

The CVS point data in the input file is sorted into a
Region NetworkLink hierarchy with the given number
of Points per region.

The input file is of this form:

score|lat|lon|name|description

A point with a higher score appears from further away.
The name becomes the Placemark's <name>.
The description becomes the Placemark's <description>
(for balloon and snippet).

"""

import os
import xml.dom.minidom
import kml.region
import kml.regionhandler
import kml.regionator
import kml.featureset
import kml.qidboxes


class BasicCSVRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self, feature_set, min_lod_pixels, maxper):

    """
    Args:
      cvslist: list of tuples 
      min_lod_pixels: minLodPixels
      maxper: maximum Features per region
    """

    self.__input_feature_set = feature_set
    self.__node_feature_set = {}
    self.__min_lod_pixels = min_lod_pixels
    self.__maxper = maxper


  def Start(self,region):

    """ RegionHandler.Start()

    Split out the Features for this region.

    The overall sort is top-down given that the pre-recursion
    method is used to split out the input items.

    """

    region_fs = self.__input_feature_set.SplitByRegion(region, self.__maxper)
    nitems = region_fs.Size()
    if nitems == 0:
      # nothing here, so nothing below either
      return [False,False]
    self.__node_feature_set[region.Qid()] = region_fs
    if nitems == self.__maxper:
      # full load here, so maybe some below too
      return [True,True]
    # nitems < self.__maxper
    # didn't max out the region so no more for child regions
    return [True,False]

  def PixelLod(self, region):
    return (self.__min_lod_pixels,-1)

  def Data(self, region):

    """ RegionHandler.Data()

    Create the KML objects for this Region.

    """

    _kml = []
    for (w,lon,lat,feature_node) in self.__node_feature_set[region.Qid()]:
      _kml.append(feature_node)  # feature_node is "<Placemark>...</Placemark>"
    return "".join(_kml)


def CDATA(cdata):
  return '<![CDATA[%s]]>' % cdata


def CreatePlacemark(id, lon, lat, name, description):
  placemark = kml.genxml.Placemark()
  placemark.name = CDATA(name)
  placemark.id = id
  placemark.description = CDATA(description)
  point = kml.genxml.Point()
  coordinates = kml.genkml.Coordinates()
  coordinates.AddPoint2(lon, lat)
  point.coordinates = coordinates.Coordinates()
  placemark.Geometry = point.xml()
  return placemark.xml()


def CreateFeatureSet(csvfile, codec):
  try:
    file = open(csvfile, 'r')
  except:
    return None
  feature_set = kml.featureset.FeatureSet()
  count = 0
  for line in file:
    tuple = line.split('|')
    score = int(tuple[0])
    lat = float(tuple[1])
    lon = float(tuple[2])
    name = tuple[3].decode(codec)
    description = tuple[4].decode(codec)
    id = 'pm%d' % count
    placemark_kml = CreatePlacemark(id, lon, lat, name, description)
    feature_set.AddWeightedFeatureAtLocation(score, lon, lat, placemark_kml)
    count += 1
  feature_set.Sort()  # Sort based on score.
  return feature_set


def RegionateCSV(inputcsv, codec, min_lod_pixels, max_per, root, dir, verbose):

  if not os.access(dir, os.W_OK):
    if verbose:
      print '%s: must exist and must be writeable' % dir
    return None

  # Read the CSV data into a FeatureSet created a Placemark for each item
  feature_set = CreateFeatureSet(inputcsv, codec)
  if not feature_set:
    return None

  csv_region_handler = BasicCSVRegionHandler(feature_set,
                                             min_lod_pixels,
                                             max_per)
  (n,s,e,w) = feature_set.NSEW()
  rtor = kml.regionator.Regionator()
  rtor.SetRegionHandler(csv_region_handler)
  rtor.SetOutputDir(dir)
  region = kml.region.RootSnap(n,s,e,w)
  rtor.SetVerbose(verbose)
  rtor.Regionate(region)

  if root:
    kml.regionator.MakeRootKML(root, region, min_lod_pixels, dir)

  kml.qidboxes.MakeQidBoxes(rtor, os.path.join(dir, 'qidboxes.kml'))

  return rtor
