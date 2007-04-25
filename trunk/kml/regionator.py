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

""" The Regionator

Core "Regionator" algorithm.

Calls out to domain-specific class derived from RegionHandler.

"""

import os

import kml.regionhandler
import kml.genkml
import kml.genxml

class Regionator:

  """

  0) Derive a class based on kml.regionhandler.RegionHandler()
  1) Create a Regionator instance
  2) SetRegionHandler()
  3) SetOutputDir() - to let Regionator() emit all KML files
  4) Regionate() - KML emitted through derived class if no output dir set
  5) MaxDepth(),QidList(),RegionCount() for post regionating info

  """

  def __init__(self):
    self._region_handler = kml.regionhandler.RegionHandler()
    self.__rootregion = 0

    self.__minFadeExtent = None
    self.__maxFadeExtent = None

    self.__minAltitude = None
    self.__maxAltitude = None
    self.__altitudeMode = None

    self.__dir = ''

    # statistics to query after regionate()
    self.__maxdepth = 0
    self.__regioncount = 0

    # list of qids in order populated
    self.__qidlist = []

    self.__timeprimitive = None

    self.__verbose = True

    self.__use_kmz = False


  def SetVerbose(self, verbose):
    self.__verbose = verbose

  def SetSaveAsKmz(self, save_as_kmz):
    self.__use_kmz = save_as_kmz


  def SetRegionHandler(self,handler):

    """

    Args:
      handler: derived from kml.regionhandler.RegionHandler()

    """

    self._region_handler = handler

  def SetOutputDir(self,dir):

    """ Set KML output directory.

    Write all KML to the specified directory.
    By default the regionhandler.Kml() method
    is instead called for each region.

    """

    self.__dir = dir

  def SetFade(self, minfade, maxfade):
    self.__minFadeExtent = minfade
    self.__maxFadeExtent = maxfade

  def SetTimePrimitive(self, tp):
    self.__timeprimitive = tp

  def SetAltitude(self, minalt, maxalt, altmode='absolute'):
    self.__minAltitude = minalt
    self.__maxAltitude = maxalt
    self.__altitudeMode = altmode

  def GetAltitude(self):
    return (self.__minAltitude, self.__maxAltitude, self.__altitudeMode)

  # Recurse on child regions returning a list
  # of children with data.
  def _Recurse(self,region):
    children = []
    for q in ['0','1','2','3']:
      r = region.Child(q)
      r = self._Regionate(r)
      if r:
        children.append(r)
    return children

  def _RegionFilename(self,region):
    if self.__use_kmz:
      return '%d.kmz' % region.Id()
    return '%d.kml' % region.Id()

  def _Regionate(self,region):
    #
    # At a given region wish to know how much data goes
    # in this region and if there are regions below
    # Three possibilities:
    # 1) no data in this region
    # 2) data in this region and one or more subregions
    # 3) data in this region, but nothing in subregions
    #
    rhandler = self._region_handler
    region.SetId(self.__regioncount + 1) # No Region has id 0
    (data_here,data_below) = rhandler.Start(region)
    if not data_here:
      return False

    # Region has data, hence it exists, hence bump counter
    self.__regioncount += 1

    # preserve traversal order of qids with data
    self.__qidlist.append(region.Qid())

    # 1) pre-recursion
    if data_below == True:
      children = self._Recurse(region)
    else:
      children = []

    # 2) This Region's Document, Style's, Schema's, TimePrimitive and Region

    document = kml.genxml.Document()
    document.name = '%d %s' % (region.Id(),region.Qid())
    
    styles = rhandler.Styles(region)
    if styles:
      document.Add_Style(styles)

    schemas = rhandler.Schemas(region)
    if schemas:
      document.Add_Schema(schemas)

    document.TimePrimitive = self.__timeprimitive

    (n,s,e,w) = region.NSEWstring()
    (minpx,maxpx) = rhandler.PixelLod(region)
    document.Region = kml.genkml.Region(n,s,e,w,
                                        minalt=self.__minAltitude,
                                        maxalt=self.__maxAltitude,
                                        altmode=self.__altitudeMode,
                                        minpx=minpx, maxpx=maxpx,
                                        minfade=self.__minFadeExtent,
                                        maxfade=self.__maxFadeExtent)

    # The Features of the region's Document: NetworkLinks and data

    # 3) NetworkLink to each child Region

    thisdepth = region.Depth()
    if thisdepth > self.__maxdepth:
      self.__maxdepth = thisdepth

    for r in children:

      networklink = kml.genxml.NetworkLink()
      networklink.name = r.Qid()

      link = kml.genxml.Link()
      link.href = self._RegionFilename(r)
      link.viewRefreshMode = 'onRegion'
      networklink.Link = link.xml()

      (n,s,e,w) = r.NSEWstring()
      (minpx,ignored) = rhandler.PixelLod(r)
      maxpx = -1 # To prevent flying under a KML hierarchy
      networklink.Region = kml.genkml.Region(n,s,e,w,
                                             minalt=self.__minAltitude,
                                             maxalt=self.__maxAltitude,
                                             altmode=self.__altitudeMode,
                                             minpx=minpx,
                                             maxpx=maxpx,
                                             minfade=self.__minFadeExtent,
                                             maxfade=self.__maxFadeExtent)

      document.Add_Feature(networklink.xml())
        
    # 4) data (Features) for this region
    
    features = rhandler.Data(region)
    document.Add_Feature(features)

    rhandler.End(region)

    k = kml.genxml.Kml()
    k.Feature = document.xml()

    kmlstr = k.xml()

    # 5) emit kml for this Region

    filename = self._RegionFilename(region)
    if self.__dir:
      path = os.path.join(self.__dir,filename)
      if self.__verbose:
        print path
      # XXX error checking...
      kmldata = kmlstr.encode('utf-8')
      if self.__use_kmz:
        kml.kmz.WriteAsKmz(kmldata, path)
      else:
        f = open(path,'w')
        f.write(kmldata)
        f.close()
    else:
      rhandler.Kml(region,filename,kmlstr)

    return region


  def Regionate(self,region):

    """ Visit this region and recurse on its children

    RegionHandler.Start() determines depth of recursion.

    Args:
      region: kml.region.Region()

    """

    self.__rootregion = region
    return self._Regionate(region)


  def MaxDepth(self):

    """
    Valid after Regionate()

    Returns:
       Max recursion depth of Region hierarchy.

    """

    return self.__maxdepth

  def RegionCount(self):

    """
    Valid after Regionate()

    Returns:
      Returns total count of Regions with data.
    """

    return self.__regioncount

  def QidList(self):

    """
    Valid after Regionate()

    Returns:
      List of qids of Regions with data in traversal order.
    """

    return self.__qidlist

  def RootRegion(self):

    """
    Returns:
      kml.region.Region: root of this Region hierarchy.
    """

    return self.__rootregion

  def LodPixels(self,region):
    return self._region_handler.PixelLod(region)

  def RootHref(self):
    root_file = self._RegionFilename(self.__rootregion)
    return '%s/%s' % (self.__dir, root_file)


def MakeRootKML(rootkml,region,lod,dir):
  """ Deprecated API.  Use MakeRootForHref() """
  return MakeRootForHref(rootkml,region,lod,'%s/1.kml'%dir)

def MakeRootForHref(rootkml,region,lod,root_href):

  """Make a NetworkLink KML file to the root

  Put the proper network URL here and publish this file.
  All NetworkLinks below are relative to this.
  
  Args:
    rootkml - name of file to create
    region - region of root of hierarchy
    lod - minLodPixels
    root_href - href to first file in hierarchy
  """

  link = kml.genxml.Link()
  link.href = root_href
  link.viewRefreshMode = 'onRegion'

  (n,s,e,w) = region.NSEWstring()
  regionxml = kml.genkml.Region(n,s,e,w,minpx=lod,maxpx=-1)

  networklink = kml.genxml.NetworkLink()
  networklink.Link = link.xml()
  networklink.Region = regionxml
  stylexml = kml.genkml.CheckHideChildren()
  networklink.Add_Style(stylexml)

  document = kml.genxml.Document()
  document.Add_Feature(networklink.xml())

  k = kml.genxml.Kml()
  k.Feature = document.xml()
  kmlstr = k.xml()

  f = open(rootkml, 'w')
  f.write(kmlstr)
  f.close()
