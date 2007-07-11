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

import os
import xml.dom.minidom
import kml.kmlparse
import kml.region
import kml.regionhandler
import kml.regionator
import kml.featureset


class KMLRegionHandler(kml.featureset.FeatureSetRegionHandler):

  def __init__(self,kmlparse,minpx,maxper):

    """
    Args:
      kmlparse: kml.kmlparse.KMLParse() with valid doc
      minpx: minLodPixels
      maxper: maximum Features per region
    """

    fs = kml.featureset.CreateFromNode(kmlparse.Doc())
    self.__style = kmlparse.ExtractDocumentStyles()
    self.__schemas = kmlparse.ExtractSchemas()
    kml.featureset.FeatureSetRegionHandler.__init__(self, fs, minpx, maxper)

  def Styles(self, region):
    # TODO: make all Style's shared and save out to common file
    return self.__style

  def Schema(self, region):
    return self.__schemas

  def Data(self, region):

    # We have our own Data because FeatureSetRegionHandler's Data
    # expects a feature in KML form.  We operate in minidom node space.

    _kml = []
    for (w,lon,lat,feature_dom_node) in self._node_feature_set[region.Qid()]:
      feature_kml = feature_dom_node.toxml()
      _kml.append(feature_kml)
    return "".join(_kml)


def RegionateKML(inputkml, min_lod_pixels, max_per, rootkml, dir, verbose):
  """Regionate a KML file

  The KML Placemarks in the input are sorted into a
  Region NetworkLink hierarchy with the given number
  of features per region.

  The RbNL sort order depends on the Placemark's Geometry:
  Point/Model: order in appearance in inputkml "most important" first.
  LineString/Polygon: order by NSEW bounding box size.
  See kml.featureset.FeatureSet().

  Args:
    input: KML file of Placemarks
    min_lod_pixels: value for <minLodPixels>
    max_per: maximum number of Placemarks per node
    rootkml: file to create to point to RbNL hierarchy
    dir: directory to write RbNL (must exist)
    verbose: if False operate silently
  Returns:
    kml.regionator.Regionator: or None if anything failed
  """

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
  if not region:
    return None
  rtor.Regionate(region)
  root_href = rtor.RootHref()

  if rootkml:
    kml.regionator.MakeRootForHref(rootkml, region, min_lod_pixels, root_href)

  return rtor
