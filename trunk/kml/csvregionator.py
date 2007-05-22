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
  """Create a CDATA section

  Args:
    arbitrary_text: as the name suggests
  Returns:
    <![CDATA[arbitrary_text]]>
  """
  return '<![CDATA[%s]]>' % cdata


def CreatePlacemark(id, lon, lat, name, description, styleUrl=None):
  """Create Point Placemark
  
  The name and description will be wrapped in CDATA sections.

  Args:
    id: value to use for id attribute of <Placemark>
    lon, lat: longitude, latitude
    name: for <Placemark>'s <name>
    description: for <Placemark>'s <description>
    styleUrl: for <Placemark>'s <styleUrl>
  Returns:
    kml: '<Placemark>...</Placemark>'
  """
  placemark = kml.genxml.Placemark()
  placemark.name = CDATA(name)
  placemark.id = id
  placemark.description = CDATA(description)
  point = kml.genxml.Point()
  coordinates = kml.genkml.Coordinates()
  coordinates.AddPoint2(lon, lat)
  point.coordinates = coordinates.Coordinates()
  placemark.Geometry = point.xml()
  if styleUrl:
    placemark.styleUrl = styleUrl
  return placemark.xml()


def ParseCsvLine(csv_line, codec):
  """
  NOTE: The csv_line is lat, lon
        The tuple is lon, lat
        The returned style_url is None if the csv_line has no such entry
  Args:
    csv_line: score|lat|lon|name|description[|style_url]
  Returns:
    tuple: (score, lon, lat, name, description, style_url)
  """
  tuple = csv_line.split('|')
  score = int(tuple[0])
  lat = float(tuple[1])
  lon = float(tuple[2])
  name = tuple[3].decode(codec)
  description = tuple[4].decode(codec)
  if len(tuple) == 6:
    styleurl = tuple[5]
  else:
    styleurl = None
  return (score, lon, lat, name, description, styleurl)

def CreateFeatureSet(csvfile, global_styleUrl, codec):
  """Create a FeatureSet from the CSV file

  Each line of the input cvsfile represents a Point Placemark.
  If global_styleUrl is not None it is used as the styleUrl for
  any line with no styleUrl of its own.  If global_styleUrl is None
  there is no styleUrl for the given line then no <styleUrl> is
  generated for that point.

  Args:
    csvfile: lines of score|lat|lon|name|description[|styleUrl]
    global_styleUrl: None or value for <styleUrl>
    codec: encoding of name and description
  Returns:
    kml.featureset.FeatureSet: or None of anything fails
  """

  try:
    file = open(csvfile, 'r')
  except:
    return None
  feature_set = kml.featureset.FeatureSet()
  count = 0
  for line in file:
    (score, lon, lat, name, description, styleUrl) = ParseCsvLine(line, codec)
    if not styleUrl and global_styleUrl:
      styleUrl = global_styleUrl
    id = 'pm%d' % count
    placemark_kml = CreatePlacemark(id, lon, lat, name, description, styleUrl)
    feature_set.AddWeightedFeatureAtLocation(score, lon, lat, placemark_kml)
    count += 1
  feature_set.Sort()  # Sort based on score.
  return feature_set


def RegionateCSV(inputcsv, codec, min_lod_pixels, max_per, root, dir, verbose,
                 global_styleUrl):
  """Regionate the given CSV file

  Args:
    inputcsv: CSV file one point per line (see CreateFeatureSet())
    codec: encoding of name and description in inputcsv
    min_lod_pixels: value for <minLodPixels>
    max_per: maximum number of items per output node
    root: KML file to create to point to RbNL hierarchy
    dir: directory write RnBNL to (must exist)
    verbose: if False operate silently, if true print generated files on stdout
    global_styleURL: value for <styleUrl> (see CreateFeatureSet())
  Returns:
    kml.regionator.Regionator: or None if anything fails
  """

  if not os.access(dir, os.W_OK):
    if verbose:
      print '%s: must exist and must be writeable' % dir
    return None

  # Read the CSV data into a FeatureSet created a Placemark for each item
  feature_set = CreateFeatureSet(inputcsv, global_styleUrl, codec)
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
