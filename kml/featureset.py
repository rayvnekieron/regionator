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
import kml.coordinates
import kml.region
import kml.regionator
import kml.regionhandler


class FeatureSet(object):

  def __init__(self):
    self.__feature_list = [] # list of (weight, lon, lat, feature) tuples

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

    """
    Returns:
      (n,s,e,w): bounding box of feature set
    """
    cbox = kml.coordbox.CoordBox()
    for (weight, lon, lat, feature) in self.__feature_list:
      cbox.AddPoint(lon, lat)
    return cbox.NSEW()

  def AddWeightedFeatureAtLocation(self, weight, lon, lat, feature):

    """
    Args:
      weight: value specifying feature importance
      lon,lat: longitude,latitude
      feature: opaque feature data
    """

    self.__feature_list.append((weight, lon, lat, feature))

  def AddFeatureAtLocation(self, lon, lat, feature):

    """
    Adds feature with 0 weight.

    Args:
      lon,lat: longitude,latitude of feature
      feature: opaque feature data
    """
    self.__feature_list.append((0, lon, lat, feature))

  def AddPoint(self, placemark_dom_node):

    """ Add the Placemark/Point to the FeatureSet

    Args:
      placemark_dom_node: minidom node for a Placemark with a Point
    Returns:
      True: Placemark and Point valid and added
      False: invalid Point Placemark not added

    """
    point_node = kml.kmlparse.GetFirstChildElement(placemark_dom_node, 'Point')
    if point_node:
      coords = kml.kmlparse.GetSimpleElementText(point_node, 'coordinates')
      if coords:
        lonlatalt = kml.coordinates.ParsePointCoordinates(coords)
        lon = lonlatalt[0]
        lat = lonlatalt[1]
        self.AddFeatureAtLocation(lon, lat, placemark_dom_node)
        return True
    return False

  def _AddCoordinatesFeature(self, geometry_dom_node, placemark_dom_node):
    coords = kml.kmlparse.GetSimpleElementText(geometry_dom_node, 'coordinates')
    if coords:
      c = kml.coordbox.CoordBox()
      c.AddCoordinates(coords)
      (lon,lat) = c.MidPoint()
      size = c.Size()
      self.AddWeightedFeatureAtLocation(size, lon, lat, placemark_dom_node)
      return True
    return False

  def AddLineString(self, placemark_dom_node):

    """ Add the Placemark/Linestring to the FeatureSet

    The Placemark represented by the minidom node placemark_dom_node
    must have a <LineString> child element which in turn must
    a <coordinates> element.

    The lon,lat of the LineString is the midpoint of the bounding box.

    The weight is the size of bounding box.

    Args:
      placemark_dom_node: minidom node for a Placemark with a LineString
    Returns:
      True: Placemark and LineString valid and added
      False: invalid LineString Placemark not added
    """

    ls_node = kml.kmlparse.GetFirstChildElement(placemark_dom_node,
                                                'LineString')
    if ls_node:
      return self._AddCoordinatesFeature(ls_node, placemark_dom_node)
    return False

  def AddPolygon(self, placemark_dom_node):

    """ Add the Placemark/Polygon to the FeatureSet

    The Placemark represented by the minidom node placemark_dom_node
    must have a <Polygon> child element which in turn must
    have an <outerBoundaryIs> element which in turn must have
    a <coordinates> element.

    The lon,lat of the Polygon is the midpoint of the bounding box
    of the outer boundary.

    The weight is the size of bounding box.

    Args:
      placemark_dom_node: minidom node for a Placemark with a Polygon
    Returns:
      True: Placemark and Polgyon valid and added
      False: invalid Polgyon Placemark not added
    """
    
    polygon_node = kml.kmlparse.GetFirstChildElement(placemark_dom_node,
                                                     'Polygon')
    if polygon_node:
      outer = kml.kmlparse.GetSimleElementText(polygon_node, 'outerBoundaryIs')
      if outer:
        return self._AddCoordinatesFeature(outer, feature_dom_node)
    return False

  def AddLocation(model_dom_node):

    """ Add the Model to the FeatureSet

    The Model must have a <Location> child element which in turn must
    have <latitude> and <longitude> child elements.
    
    Args:
      placemark_dom_node: minidom node for a Placemark with a Model
    Returns:
      True: Placemark and Model valid and added
      False: invalid Model Placemark not added
    """
    location_node = kml.kmlparse.GetFirstChildElement(model_dom_node,
                                                      'Location')
    if location_node:
      location = kml.kmlparse.ParseLocation(location_node)
      if location:
        self.AddFeatureAtLocation(location.longitude,
                                  location.latitude,
                                  feature_dom_node)
        return True
    return False

  def AddFeature(self, feature_dom_node):

    """ Add the xml minidom representation of the Feature.

    Feature must be a Placemark with either Point, LineString,
    Polygon or Model Geometry.

    This is how each Geometry is added:

    Point: lon,lat is taken from the coordinates element.
    The weight is 0.

    LineString: lon,lat is the midpoint of the bounding box of
    the coordinates.  The weight is the size of the bounding box.

    Polygon: lon, lat, is midpoint of the bounding box of the
    coordinates of the outer boundary (<outerBoundaryIs> element).
    The weight is the size of the bounding box.

    Model: lon,lat is given by the <longitude> and <latitude>
    children of <Location>.  The weight is 0.

    If feature_dom_node does not have one of the above child elements
    or if the appropriate element describing the lon,lat is not
    found the feature is not added and False is returned.
    
    Args:
      feature_dom_node: minidom node of a KML Feature
    Returns:
      True: Feature valid and was added
      False: Feature not valid and not added
    """

    if self.AddPoint(feature_dom_node) or \
       self.AddLineString(feature_dom_node) or \
       self.AddPolygon(feature_dom_node) or \
       self.AddLocation(feature_dom_node):
      return True
    return False

  def CopyByRegion(self, region):

    """Creates a new FeatureSet for features within the region

    The FeatureSet is unchanged.

    Args:
      region: kml.region.Region()

    Returns:
      featureset: kml.featureset.FeatureSet
    """

    fs = FeatureSet()
    for (weight, lon, lat, feature_node) in self.__feature_list:
      if region.InRegion(lon, lat):
        fs.AddWeightedFeatureAtLocation(weight, lon, lat, feature_node)
    return fs


  def SplitByRegion(self, region, max=None):

    """Moves features in the region into a new FeatureSet

    NOTE: This is destructive.  The features are DELETED
    from the FeatureSet.  Use CopyByRegion() to preserve the FeatureSet.

    Args:
      region: kml.region.Region()
      max: maximum number of features to split out, no limit if None

    Returns:
      featureset: kml.featureset.FeatureSet
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


class FeatureSetRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self, feature_set, min_lod_pixels, maxper):

    """
    Args:
      feature_set: kml.featureset.FeatureSet of KML Features
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
    for (w,lon,lat,feature_kml) in self.__node_feature_set[region.Qid()]:
      _kml.append(feature_kml)  # feature_node is "<Placemark>...</Placemark>"
    return "".join(_kml)


