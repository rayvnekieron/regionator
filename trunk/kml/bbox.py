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

import kml.kmlparse
import kml.coordbox

def GetCoordinatesBBOX(parent_node):
  """
  Args:
    parent_node: minidom node of parent of coordinates
  Returns:
    (n,s,e,w):
  """
  coords = kml.kmlparse.GetSimpleElementText(parent_node, 'coordinates')
  if not coords:
    return None
  c = kml.coordbox.CoordBox()
  c.AddCoordinates(coords)
  return c.NSEW()

def GetPolygonBBOX(polygon_node):
  outer = kml.kmlparse.GetFirstChildElement(polygon_node, 'outerBoundaryIs')
  if not outer:
    return None
  return GetCoordinatesBBOX(outer)

def GetPointBBOX(lon, lat):
  # XXX
  return (lat + .01, lat - .01, lon + .01, lat + .01)

def GetModelBBOX(model_node):
  # NOTE: Location is quite often not where the actual model is
  location_node = kml.kmlparse.GetFirstChildElement(placemark_node, 'Location')
  if location_node:
    lon = kml.kmlparse.GetSimpleElementText(location_node, 'longitude')
    lat = kml.kmlparse.GetSimpleElementText(location_node, 'latitude')
    return GetPointBBOX(lon, lat)
  return None

def GetMultiGeometryBBOX(multigeometry):
  """ TODO
  fs = kml.featureset.FeatureSet()
  for node in multigeometry:
  """

def GetPlacemarkBBOX(placemark):
  """
  Args:
    placemark: minidom node of a Placemark
  Returns:
    (n,s,e,w):
  """
  polygon = kml.kmlparse.GetFirstChildElement(placemark, 'Polygon')
  if polygon:
    return GetPolygonBBOX(polygon)
  linestring = kml.kmlparse.GetFirstChildElement(placemark, 'LineString')
  if linestring:
    return GetCoordinatesBBOX(linestring)
  linearring = kml.kmlparse.GetFirstChildElement(placemark, 'LinearRing')
  if linearring:
    return GetCoordinatesBBOX(linearring)
  point = kml.kmlparse.GetFirstChildElement(placemark, 'Point')
  if point:
    return GetPointBBOX(point)
  model = kml.kmlparse.GetFirstChildElement(placemark, 'Model')
  if model:
    return GetModelBBOX(model)
  multigeometry = kml.kmlparse.GetFirstChildElement(placemark, 'MultiGeometry')
  if multigeometry:
    return GetMultiGeometryBBOX(multigeometry)
  return None
