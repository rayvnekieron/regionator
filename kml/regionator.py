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

#import kml.region
import kml.regionhandler
import kml.genkml
import kml.version

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
    self.__minfade = 0
    self.__maxfade = 0

    self.__dir = ''

    # statistics to query after regionate()
    self.__maxdepth = 0
    self.__regioncount = 0

    # list of qids in order populated
    self.__qidlist = []

    self.__timeprimitive = None


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

  def SetFade(self,minfade,maxfade):
    self.__minfade = minfade
    self.__maxfade = maxfade

  def SetTimePrimitive(self, tp):
    self.__timeprimitive = tp

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

    # 2) This Region

    _kml = []
    _kml.append(kml.genkml.KML21())
    _kml.append('<!-- Regionator %s -->\n' % kml.version.Revision())
    _kml.append('<Document>\n')
    _kml.append('<name>%d %s</name>\n' % (region.Id(),region.Qid()))
    
    # XXX Schema's and Style's go here...

    _kml.append('\n')
    (n,s,e,w) = region.NSEW()
    (minpx,maxpx) = rhandler.PixelLod(region)
    minfade = self.__minfade
    maxfade = self.__maxfade
    _kml.append(kml.genkml.Region(n,s,e,w,minpx=minpx,maxpx=maxpx,minfade=minfade,maxfade=maxfade))

    # 2) NetworkLink to each child Region

    thisdepth = region.Depth()
    if thisdepth > self.__maxdepth:
      self.__maxdepth = thisdepth
    for r in children:
      (minpx,maxpx) = rhandler.PixelLod(r)
      (n,s,e,w) = r.NSEW()
      href = self._RegionFilename(r)
      _kml.append('\n')
      _kml.append(kml.genkml.RegionNetworkLink(n,s,e,w,r.Qid(),href,minpx,maxpx))
        
    # 3) data for this region

    if self.__timeprimitive:
      _kml.append('\n<Folder>\n')
      _kml.append(self.__timeprimitive)
    
    _kml.append(rhandler.Data(region))

    if self.__timeprimitive:
      _kml.append('</Folder>\n')

    rhandler.End(region)

    _kml.append('</Document>\n')
    _kml.append('</kml>\n')

    kmlstr = "".join(_kml)

    # 4) emit kml for this Region

    filename = self._RegionFilename(region)
    if self.__dir:
      path = os.path.join(self.__dir,filename)
      print path
      # XXX error checking...
      f = open(path,'w')
      f.write(kmlstr.encode('utf-8'))
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


def MakeRootKML(rootkml,region,lod,dir):

  """Make a NetworkLink KML file to the root

  Put the proper network URL here and publish this file.
  All NetworkLinks below are relative to this.
  
  Args:
    rootkml - name of file to create
    region - region of root of hierarchy
    dir - hierarchy directory
  """

  _kml = []
  _kml.append(kml.genkml.KML21())
  _kml.append('<Document>\n')
  _kml.append(kml.genkml.CheckHideChildren(id='docstyle'))

  # A 2nd level Folder to ensure checkHideChildren-ness
  # as a NetworkLink load discards the Document and hence
  # the checkHideChildren-ness it otherwise provides.

  _kml.append('<Folder>\n')
  _kml.append(kml.genkml.CheckHideChildren())

  (n,s,e,w) = region.NSEW()
  href = '%s/1.kml' % dir
  maxpixels = -1
  _kml.append(kml.genkml.RegionNetworkLink(n,s,e,w,'root',href,lod,maxpixels))

  _kml.append('</Folder>\n')
  _kml.append('</Document>\n')
  _kml.append('</kml>\n')

  f = open(rootkml, 'w')
  f.write("".join(_kml))
  f.close()
