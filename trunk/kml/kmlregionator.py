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

""" SimpleKMLRegionHandler

A Regionator of KML input data.

The KML Features in the input are sorted into a
Region NetworkLink hierarchy with the given number
of features per region.

"""

import os
import xml.dom.minidom
import kml.kmlparse
import kml.region
import kml.regionhandler
import kml.regionator
import kml.featureset


class KMLRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self,kmlparse,minpx,maxper):

    """
    Args:
      kmlparse: kml.kmlparse.KMLParse() with valid doc
      minpx: minLodPixels
      maxper: maximum Features per region
    """

    self._Parse(kmlparse.Doc())
    self.__style = kmlparse.ExtractDocumentStyles()
    self.__schemas = kmlparse.ExtractSchemas()
    self.__node_feature_set = {}
    self.__minpx = minpx
    self.__maxper = maxper

  def _Parse(self, doc):
    fs = kml.featureset.FeatureSet()
    for placemark_node in doc.getElementsByTagName('Placemark'):
      fs.AddFeature(placemark_node)
    self.__input_feature_set = fs

  def NSEW(self):
    return self.__input_feature_set.NSEW()

  def Start(self,region):

    """ RegionHandler.Start()

    Split out the Features for this region.

    The overall sort is top-down given that the pre-recursion
    method is used to split out the input items.

    """

    fs = self.__input_feature_set.SplitByRegion(region, self.__maxper)
    nitems = fs.Size()
    if nitems == 0:
      # nothing here, so nothing below either
      return [False,False]
    self.__node_feature_set[region.Qid()] = fs
    if nitems == self.__maxper:
      # full load here, so maybe some below too
      return [True,True]
    # nitems < self.__maxper
    # didn't max out the region so no more for child regions
    return [True,False]

  def Styles(self, region):
    # TODO: make all Style's shared and save out to common file
    return self.__style

  def Schema(self, region):
    return self.__schemas

  def Data(self,region):

    """ RegionHandler.Data()

    Create the KML objects for this Region.

    """

    _kml = []
    for (w,lon,lat,feature_node) in self.__node_feature_set[region.Qid()]:
      _kml.append(feature_node.toxml())
    return "".join(_kml)

  def PixelLod(self,region):

    """ RegionHandler.PixelLod()

    KML objects accumulate down the hierarchy: items at the coarsest
    level of hierarchy are visible to the finest level.  This is
    achieved through the use of maxLodPixels = -1.

    """

    maxPixels = -1 # visible to 0 range
    minPixels = self.__minpx
    return (minPixels,maxPixels)


def RegionateKML(inputkml, min_lod_pixels, max_per, rootkml, dir, verbose):

  if not os.access(dir, os.W_OK):
    if verbose:
      print '%s: must exist and must be writeable' % dir
    return None

  kml_parse = kml.kmlparse.KMLParse(inputkml)
  if not kml_parse.Doc():
    if verbose:
      print '%s: parse failed' % inputkml
    return None

  kml_region_handler = KMLRegionHandler(kml_parse, min_lod_pixels, max_per)
  (n,s,e,w) = kml_region_handler.NSEW()
  rtor = kml.regionator.Regionator()
  rtor.SetRegionHandler(kml_region_handler)
  rtor.SetOutputDir(dir)
  rtor.SetVerbose(verbose)
  region = kml.region.RootSnap(n,s,e,w)
  rtor.Regionate(region)

  kml.regionator.MakeRootKML(rootkml, region, min_lod_pixels, dir)

  return rtor
