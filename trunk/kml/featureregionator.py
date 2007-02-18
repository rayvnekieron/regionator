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

""" class FeatureRegionator

"""

import os

import kml.coordbox
import kml.simpleregionator
import kml.genkml
import kml.kmlparse
import kml.coordinates

class FeatureRegionator:

  """Base class for Regionating existing KML documents

  1) Derive a class from this
  2) Derived class should implement ExtractItems() which
     should use Add*() to define the dataset bounding box, and
  3) AddItem() on each KML object.

  """

  def __init__(self):
    self.__cbox = kml.coordbox.CoordBox()
    self.__items = []
    self.__weighted_items = [] # XXX
    # XXX duplicating stuff in Regionator...
    self.__minfade = 0
    self.__maxfade = 0
    self.__verbose = True

  def SetVerbose(self, verbose):
    self.__verbose = verbose

  def GetVerbose(self):
    return self.__verbose

  def SetFade(self,minfade,maxfade):
    self.__minfade = minfade
    self.__maxfade = maxfade

  # Returns latlonbox (n,s,e,w) of extracted items
  # Intended for use after extractitems, regionate
  def NSEW(self):
    return self.__cbox.NSEW()

  def GetDoc(self):

    """Gets DOM tree of parsed KML

    Valid only after Regionate()

    Returns:
      doc: xml.dom.minidom.parse

    """

    if self.__kmlparse:
      return self.__kmlparse.Doc()
    return None

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

  def ExtractItems(self):
    """subclass for feature-specific items.  Placemark/Point, etc"""
    """save tuples (lon+lat,feature-kml) with AddItem()"""
    """call Add*() to compute overall bbox"""

  def Regionate(self,kmlfile,lod,per,rootkml,dir):

    """

    Args:
      kmlfile: pathname of input KML file (read only)
      lod: value for minLodPixels
      per: maximum number of items for each region
      rootkml: path of file to create to point to generated KML hierarchy
      dir: directory to save KML hierarchy

    Returns:
      rtor: kml.regionator
    """

    os.makedirs(dir)

    if self.__verbose == True:
      print 'parsing...'
    self.__kmlparse = kml.kmlparse.KMLParse(kmlfile)
    if not self.__kmlparse.Doc():
      return

    if self.__verbose:
      print 'extracting items...'
    self.ExtractItems()

    self._SortItems()

    if len(self.__items) == 0:
      if self.__verbose:
        print 'no items extracted?'
      return None

    (n,s,e,w) = self.__cbox.NSEW()

    if self.__verbose:
      print 'regionating',n,s,e,w
    style_kml = self.__kmlparse.ExtractDocumentStyles()
    schema_kml = self.__kmlparse.ExtractSchemas()
    rtor = kml.simpleregionator.Regionate(n,s,e,w,lod,per,
                                          self.__items,
                                          dir,
                                          style=style_kml,
                                          schema=schema_kml,
                                          minfade=self.__minfade,
                                          maxfade=self.__maxfade,
                                          verbose=self.__verbose)

    kml.regionator.MakeRootKML(rootkml,rtor.RootRegion(),lod,dir)

    return rtor

  def _SaneLoc(self,lon,lat):
    if lon < -180.0 or lon > 180.0 or lat < -90.0 or lat > 90.0:
      if self.__verbose:
        print 'bad lon/lat',lon,lat
      return False
    return True

  def _AddLoc(self,lon,lat):
    if self._SaneLoc(lon,lat):
      self.__cbox.AddPoint(lon,lat)
      # return '%f+%f' % (lon,lat)
      return kml.latlon.Point(lon,lat)
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
    return (size,lonlat)

  def AddLocation(self,loc):
    (long,latf) = kml.kmlparse.ParseLocation(loc)
    return self._AddLoc(lonf,latf)

