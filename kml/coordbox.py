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


""" class CoordBox

Incrementally sweep out the bounding box for a set of points.

1) Create an instance of CoordBox.
2) Add points using AddPoint() and/or AddCoordinates()
3) Inquire resulting bounding box extent, size and center

"""

import math

import kml.coordinates


class CoordBox:

  """ Keep track of the box around a bunch of coordinates

  Add points with AddPoint(lon,lat) and/or AddCoordinates(<coordinates>)
  AddPoint and AddCoordinates merely stretch the bbox to fit.
  No specific point is recorded.

  MidPoint(), NSEW(), and Size() return information about
  the resulting bbox.

  """

  def __init__(self):
    self._n = -90
    self._s = 90
    self._e = -180
    self._w = 180

  def AddPoint(self,lon,lat):

    """

    Args:
      lon,lat: decimal degrees float

    """

    if lat > self._n:
      self._n = lat
    if lat < self._s:
      self._s = lat
    if lon > self._e:
      self._e = lon
    if lon < self._w:
      self._w = lon

  def AddCoordinates(self,coordinates):

    """ Add a list of coordinates

    Calls AddPoint for each coordinate in the list.

    Args:
      coordinates: string of space separated lon,lat,alt triples
                   (value of <coordinates>)

    """

    pointlist = kml.coordinates.ParseCoordinates(coordinates)
    for point in pointlist:
      self.AddPoint(point[0], point[1])


  def MidPoint(self):

    """ The geographic center of the CoordBox

    Returns:
      (lon,lat)

    """

    lon = (self._e + self._w)/2
    lat = (self._n + self._s)/2
    return (lon,lat)

  def NSEW(self):

    """ The bounding box of the CoordBox

    Returns:
      (n,s,e,w)

    """

    return (self._n, self._s, self._e, self._w)

  def Size(self):

    """ Size of CoordBox

    This bears some relation to Region Lod min/maxLodPixels.

    This is intended as the basis for relative size comparison in
    a given geographic region.

    Too simplistic for use over a broad a range of latitudes --
    consider the _pixel_ width of an N degree square at the equator vs a pole.

    Returns:
      val: square root of area expressed in degrees
           (width in degrees of a square CoordBox)

    """

    wid = self._n - self._s
    ht = self._e - self._w
    return math.sqrt(wid * ht)

