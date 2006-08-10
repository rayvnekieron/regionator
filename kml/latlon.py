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

""" class LatLonBox

"""


class LatLonBox:
  def __init__(self,n,s,e,w):
    self.SetNSEW(n,s,e,w)

  def SetNSEW(self,n,s,e,w):
    self.__n = n
    self.__s = s
    self.__e = e
    self.__w = w

  def NSEW(self):
    return (self.__n,self.__s,self.__e,self.__w)

  def ValidNSEW(self):

    """Is bounding box valid?

    Returns:
      Boolean:
    """

    return self.__n > self.__s and self.__e > self.__w


  def HasPixels(self,n,s,e,w):
    if self.__n > s and self.__s < n and self.__e > w and self.__w < e:
      return True
    return False

  def IsPartial(self,n,s,e,w):
    if w < self.__w or e > self.__e or n > self.__n or s < self.__s:
      return True
    return False

def Point(lon,lat):

  """ Format a lon+lat string

  Args:
    lon,lat: decimal degress

  Returns:
    String unique to the given lon,lat

  """

  return '%f+%f' % (lon,lat)

def SplitPoint(point):

  """ Parse a lon+lat string

  Args:
    lon+lat string

  Returns:
    (lon,lat) in floating point decimal degrees

  """

  ps = point.split('+')
  lon = float(ps[0])
  lat = float(ps[1])
  return (lon,lat)

def DecimalDegrees(degrees, minutes, seconds):

  """Convert DMS to decimal degrees

  input: 33 8' 59.53" (33, 8, 59.53)

  output: 33.149869444444441

  Args:
    degrees: int
    minutes: int
    seconds: float

  Returns:
    decimal_degrees: float
  """

  minutes = minutes + seconds/60.
  decimal = minutes/60.
  return degrees + decimal

