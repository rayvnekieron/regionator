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
import kml.featurequeue


def Regionate(n,s,e,w,
              minpx, per, featureq, dir,
              style='', schema='', minfade=0, maxfade=0,
              verbose=True):

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
  rtor.SetRegionHandler(SimpleRegionHandler(featureq,minpx,per,style,schema))
  rtor.SetOutputDir(dir)
  rtor.SetFade(minfade,maxfade)
  rtor.SetVerbose(verbose)

  # snap the region to the smallest enclosing earth-native region
  r = kml.region.RootSnap(n,s,e,w)

  rtor.Regionate(r)
  return rtor


class SimpleRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self,featureq,minpx,per,style,schema):
    self.__featureq = featureq
    self.__minpx = minpx
    self.__maxper = per
    self.__qid_items = {}
    self.__style = style
    self.__schema = schema

  def Start(self,region):

    """ RegionHandler.Start()

    Split out the objects for this region.

    The overall sort is top-down given that the pre-recursion
    method is used to split out the input items.

    """

    ritems = self.__featureq.Split(region, self.__maxper)
    nitems = len(ritems)
    if nitems == 0:
      # nothing here, so nothing below either
      return [False,False]
    self.__qid_items[region.Qid()] = ritems
    if nitems == self.__maxper:
      # full load here, so maybe some below too
      return [True,True]
    # nitems < self.__maxper
    # didn't max out the region so no more for child regions
    return [True,False]

  def Styles(self, region):
    return self.__style

  def Schema(self, region):
    return self.__schema

  def Data(self,region):

    """ RegionHandler.Data()

    Create the KML objects for this Region.

    """

    _kml = []

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

