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

import kml.featurequeue
import kml.kmlparse
import kml.simpleregionator

class FeatureRegionator(kml.featurequeue.FeatureQueueX):

  """Base class for Regionating existing KML documents

  1) Derive a class from this
  2) Derived class should implement ExtractItems() which
     should use Add*() to define the dataset bounding box, and
  3) AddItem() on each KML object.

  """

  def __init__(self):
    kml.featurequeue.FeatureQueueX.__init__(self)
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

  def GetDoc(self):

    """Gets DOM tree of parsed KML

    Valid only after Regionate()

    Returns:
      doc: xml.dom.minidom.parse

    """

    if self.__kmlparse:
      return self.__kmlparse.Doc()
    return None

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

    items = self._Items()
    if len(items) == 0:
      if self.__verbose:
        print 'no items extracted?'
      return None

    (n,s,e,w) = self.NSEW()

    if self.__verbose:
      print 'regionating',n,s,e,w
    style_kml = self.__kmlparse.ExtractDocumentStyles()
    schema_kml = self.__kmlparse.ExtractSchemas()
    rtor = kml.simpleregionator.Regionate(n,s,e,w,lod,per,
                                          self,  # as a FeatureQueue
                                          dir,
                                          style=style_kml,
                                          schema=schema_kml,
                                          minfade=self.__minfade,
                                          maxfade=self.__maxfade,
                                          verbose=self.__verbose)

    kml.regionator.MakeRootKML(rootkml,rtor.RootRegion(),lod,dir)

    return rtor

