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

# Create a Region NetworkLink hierarchy to a set of Models

import os

import kml.region
import kml.regionhandler
import kml.regionator
import kml.model
import kml.featureset


class BasicModelRegionHandler(kml.regionhandler.RegionHandler):

  def __init__(self, nodemax, feature_set, dir):
    self.__nodemax = nodemax
    self.__feature_set = feature_set
    self.__dir = dir
    self.__node_feature_set = {}

  def Start(self, region):

    """
    If there are more than "nodemax" models in this region
    create links to children for them to consider.
    """

    fs = self.__feature_set.CopyByRegion(region)
    count = fs.Size()
    if count > self.__nodemax:
      # Too many for this node, push amongst children
      # XXX search each child to avoid building unecessary networklinks...
      return [True,True]

    # Maximum not exceeded, recurse no further
    self.__node_feature_set[region.Qid()] = fs
    return [True,False]


  def Data(self, region):
    if not self.__node_feature_set.has_key(region.Qid()):
      return "" # XXX prune out no-data child kmls

    # A Folder to fill with one NetworkLink per Model kmz
    folder = kml.genxml.Folder()

    for (w,lon,lat,model) in self.__node_feature_set[region.Qid()]:

      # Create the NetworkLink to the kmz
      networklink = kml.genxml.NetworkLink()
      link = kml.genxml.Link()
      link.href = '../%s' % model.Kmz()
      networklink.Link = link.xml()

      # Add the NetworkLink to the Folder
      folder.Add_Feature(networklink.xml())

    return folder.xml()


def BasicModelRegionator(modeldir, rootkml, outputdir):

  """
  Args:
    modeldir: a directory of .kmz's
    rootkml: networklink kml to root of kml hierarchy
    outputdir: directory kml is written
  """

  modelset = kml.model.ModelSet(modeldir)
  modelset.FindAndParse()
  featureset = modelset.FeatureSet()
  (n,s,e,w) = modelset.FindBBOX()
  mrhandler = BasicModelRegionHandler(8, featureset, modeldir)
  rtor = kml.regionator.Regionator()
  rtor.SetRegionHandler(mrhandler)
  rtor.SetOutputDir(outputdir)
  os.makedirs(outputdir)
  root = kml.region.RootSnap(n,s,e,w)
  print 'Regionating...'
  rtor.Regionate(root)
  kml.regionator.MakeRootKML(rootkml, root, 256, outputdir)
