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

""" SimpleRegionHandler

A generic Regionator of existing KML data.

This inputs a list of located KML objects and sorts it into
a Region NetworkLink hierarchy with the given number
of objects per Region.

"""


import kml.region
import kml.regionhandler
import kml.regionator
import kml.latlon


def Regionate(n,s,e,w,minpx,per,items,dir,style='',schema='',minfade=0,maxfade=0):

  """ Creates a KML Region hierarchy top down in list order.

  Args:
    item: (loc,kmlfeature)
      loc: '%f+%f' % (lon,lat)
      kmlfeature: '<Placemark>...</Placemark>'
    n,s,e,w: root region
    minpx: minLodPixels, (maxLodPixels = -1 in simpleRegionator)
    per: items per region
    dir: where to write the kml files
    style: '<Style>...</Style>'
    schema: '<Schema>...</Schema>'
  """

  rtor = kml.regionator.Regionator()
  rtor.SetRegionHandler(SimpleRegionHandler(items,minpx,per,style,schema))
  rtor.SetOutputDir(dir)
  rtor.SetFade(minfade,maxfade)

  # snap the region to the smallest enclosing earth-native region
  r = kml.region.RootSnap(n,s,e,w)

  rtor.Regionate(r)
  return rtor


class SimpleRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self,items,minpx,per,style,schema):
    self.__items = items
    self.__minpx = minpx
    self.__maxper = per
    self.__qid_items = {}
    self.__style = style
    self.__schema = schema


  def _Split(self,region):

    """

    Finds the first '__maxper' objects within this Region,
    stores them to the _qid_items dictionary index by
    the qid, and _removes_ them from the __items list.

    Returns:
      num: number of items found for this Region.

    """
    
    (n,s,e,w) = region.NSEW()
    ritems = []
    index = 0
    nitems = self.__maxper
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
    # save the items in this region
    self.__qid_items[region.Qid()] = ritems
    return ritems.__len__()

  def Start(self,region):

    """ RegionHandler.Start()

    Split out the objects for this region.

    The overall sort is top-down given that the pre-recursion
    method is used to split out the input items.

    """

    nitems = self._Split(region)
    if nitems == 0:
      # nothing here, so nothing below either
      return [False,False]
    if nitems == self.__maxper:
      # full load here, so maybe some below too
      return [True,True]
    # nitems < self.__maxper
    # didn't max out the region so no more for child regions
    return [True,False]

  def Data(self,region):

    """ RegionHandler.Data()

    Create the KML objects for this Region.

    """

    _kml = []

    # XXX move above Document's Region (above NetworkLinks)

    if self.__style:
      _kml.append(self.__style)
    if self.__schema:
      _kml.append(self.__schema)

    ritems = self.__qid_items[region.Qid()]
    for item in ritems:
      _kml.append(item[1])
    return "".join(_kml)

  def PixelLod(self,region):

    """ RegionHandler.PixelLod()

    KML objects accumulate down the hierarchy: items at the coarsest
    level of hierarchy are visible to the finest level.  This is
    achieved through the use of maxLodPixels = -1.

    """

    maxPixels = -1 # visible to 0 range
    minPixels = self.__minpx
    return (minPixels,maxPixels)

