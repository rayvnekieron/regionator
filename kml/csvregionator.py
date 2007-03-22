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

import os
import kml.region
import kml.regionator
import kml.featureset
import kml.qidboxes


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

  feature_set_handler = kml.featureset.FeatureSetRegionHandler(feature_set,
                                                               min_lod_pixels,
                                                               max_per)
  (n,s,e,w) = feature_set.NSEW()
  rtor = kml.regionator.Regionator()
  rtor.SetRegionHandler(feature_set_handler)
  rtor.SetOutputDir(dir)
  region = kml.region.RootSnap(n,s,e,w)
  rtor.SetVerbose(verbose)
  rtor.Regionate(region)

  if root:
    kml.regionator.MakeRootKML(root, region, min_lod_pixels, dir)

  kml.qidboxes.MakeQidBoxes(rtor, os.path.join(dir, 'qidboxes.kml'))

  return rtor
