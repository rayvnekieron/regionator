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

import kml.coordbox
import kml.region
import kml.coordinates


class FeatureSet(object):

  def __init__(self):
    self.__feature_list = [] # list of (weight, lon, lat, feature_node) tuples

  def __iter__(self):
    self.__index = 0
    return self

  def next(self):
    index = self.__index
    if index == len(self.__feature_list):
      raise StopIteration
    else:
      self.__index += 1
      return self.__feature_list[index]

  def Size(self):
    return len(self.__feature_list)

  def GetFeature(self, index):
    if index < len(self.__feature_list):
      return self.__feature_list[index][3]
    return None

  def GetLoc(self, index):
    """
    Returns:
      (lon,lat)
    """
    if index < len(self.__feature_list):
      feature = self.__feature_list[index]
      return (feature[1], feature[2])
    return None

  def NSEW(self):
    cbox = kml.coordbox.CoordBox()
    for (weight, lon, lat, feature_node) in self.__feature_list:
      cbox.AddPoint(lon, lat)
    return cbox.NSEW()

  def AddWeightedFeatureAtLocation(self, weight, lon, lat, feature_node):
    self.__feature_list.append((weight, lon, lat, feature_node))

  def AddFeatureAtLocation(self, lon, lat, feature_node):
    self.__feature_list.append((0, lon, lat, feature_node))

  def AddPoint(self, feature_node):
    point_node = kml.kmlparse.GetFirstChildElement(feature_node, 'Point')
    if point_node:
      coords = kml.kmlparse.GetSimpleElementText(point_node, 'coordinates')
      if coords:
        lonlatalt = kml.coordinates.ParsePointCoordinates(coords)
        lon = lonlatalt[0]
        lat = lonlatalt[1]
        self.AddFeatureAtLocation(lon, lat, feature_node)
        return True
    return False

  def AddCoordinatesFeature(self, geometry_node, feature_node):
    coords = kml.kmlparse.GetSimpleElementText(geometry_node, 'coordinates')
    if coords:
      c = kml.coordbox.CoordBox()
      c.AddCoordinates(coords)
      (lon,lat) = c.MidPoint()
      size = c.Size()
      self.AddWeightedFeatureAtLocation(size, lon, lat, feature_node)
      return True
    return False

  def AddLineString(self, feature_node):
    ls_node = kml.kmlparse.GetFirstChildElement(feature_node, 'LineString')
    if ls_node:
      return self.AddCoordinatesFeature(ls_node, feature_node)
    return False

  def AddPolygon(self, feature_node):
    polygon_node = kml.kmlparse.GetFirstChildElement(feature_node, 'Polygon')
    if polygon_node:
      outer = kml.kmlparse.GetSimleElementText(polygon_node, 'outerBoundaryIs')
      if outer:
        return self.AddCoordinatesFeature(outer, feature_node)
    return False

  def AddLocation(feature_node):
    location_node = kml.kmlparse.GetFirstChildElement(feature_node, 'Location')
    if location_node:
      location = kml.kmlparse.ParseLocation(location_node)
      if location:
        self.AddFeatureAtLocation(location.longitude,
                                  location.latitude,
                                  feature_node)
        return True
    return False

  def AddFeature(self, feature_node):
    if self.AddPoint(feature_node) or \
       self.AddLineString(feature_node) or \
       self.AddPolygon(feature_node) or \
       self.AddLocation(feature_node):
      return True
    return False

  def CopyByRegion(self, region):

    """Returns a FeatureSet of features within the region

    The FeatureSet is unchanged.

    Args:
      region: kml.region.Region()

    Returns:
      featureset: kml.featureset.FeatureSet()
    """

    fs = FeatureSet()
    for (weight, lon, lat, feature_node) in self.__feature_list:
      if region.InRegion(lon, lat):
        fs.AddWeightedFeatureAtLocation(weight, lon, lat, feature_node)
    return fs


  def SplitByRegion(self, region, max=None):

    """Moves features in the region into a new FeatureSet

    Args:
      region: kml.region.Region()
      max: maximum number of features to split out, no limit if None

    Returns:
      featureset: kml.featureset.FeatureSet()
    """

    if max == None:
      max = len(self.__feature_list)
    fs = FeatureSet()
    index = 0
    while max and index < len(self.__feature_list):
      (weight, lon, lat, feature_node) = self.__feature_list[index]
      if region.InRegion(lon, lat):
        fs.AddWeightedFeatureAtLocation(weight, lon, lat, feature_node)
        self.__feature_list.pop(index)
        max -= 1
      else:
        index += 1
    return fs

  def Sort(self):
    """Sort this FeatureSet largest weight first"""
    self.__feature_list.sort()
    self.__feature_list.reverse()
