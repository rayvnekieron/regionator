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

""" class FeatureQueue

"""

import kml.coordbox
import kml.region
import kml.latlon
import kml.coordinates

class FeatureQueueX(object):

  def __init__(self):
    self.__cbox = kml.coordbox.CoordBox()
    self.__items = []
    self.__weighted_items = [] # XXX
    self.__verbose = False

  def _Items(self):
    return self.__items

  def Split(self,region,nitems):
  
    """

    Returns the first 'nitems' objects within this Region,
    removing them from the queue.

    Returns:
      num: list of items

    """

    (n,s,e,w) = region.NSEW()
    ritems = []
    index = 0
    # This (unfortunately) searches the whole __items list
    # in trying to fill out the maximum.
    while nitems and index < self.__items.__len__():
      tryitem = self.__items[index]
      (lon,lat) = kml.latlon.SplitPoint(tryitem[0])
      if region.InRegion(lon,lat):
        gotitem = self.__items.pop(index)
        ritems.append(gotitem)
        nitems -= 1
      else:
        # increment index if we didn't shrink the list
        index += 1
    # return the items split out for this Region
    return ritems


  # Returns latlonbox (n,s,e,w) of extracted items
  # Intended for use after extractitems, regionate
  def NSEW(self):
    return self.__cbox.NSEW()

  def _SortItems(self):
    num = self.__weighted_items.__len__()
    if num == 0:
      return
    # sorts smallest to largest
    if self.__verbose:
      print 'sorting %d items...' % num
    self.__weighted_items.sort()
    for i in self.__weighted_items:
      item = (i[1],i[2])
      # put new item at head of list
      self.__items.insert(0,item)
      
  def AddWeightedItem(self,item):
  
    """
    
    Args:
      item = (weight,lon+lat,kml)
    """
    self.__weighted_items.append(item)
    
  # item = (lon+lat,kml)
  def AddItem(self,item):
    self.__items.append(item)

  def _SaneLoc(self,lon,lat):
    if lon < -180.0 or lon > 180.0 or lat < -90.0 or lat > 90.0:
      if self.__verbose:
        print 'bad lon/lat',lon,lat
      return False
    return True

  def _AddLoc(self,lon,lat):
    if self._SaneLoc(lon,lat):
      self.__cbox.AddPoint(lon,lat)
      return kml.latlon.Point(lon,lat) # XXX call AddItem
    return ''

  def AddPointCoordinates(self,cml):
    text = kml.kmlparse.GetText(cml)
    points = kml.coordinates.ParseCoordinates(text)
    if points:
      point = points[0]
      return self._AddLoc(point[0], point[1])
    return None

  def AddLinestringCoordinates(self,cml):
    text = kml.kmlparse.GetText(cml)
    if text.__len__() == 0:
      return ''
    c = kml.coordbox.CoordBox()
    c.AddCoordinates(text)
    [lon,lat] = c.MidPoint()
    size = c.Size()
    lonlat = self._AddLoc(lon,lat)
    return (size,lonlat) # XXX call AddWeightedItem

  def AddLocation(self,loc):
    (long,latf) = kml.kmlparse.ParseLocation(loc)
    return self._AddLoc(lonf,latf)


