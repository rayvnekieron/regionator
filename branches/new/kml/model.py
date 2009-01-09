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

import os
import os.path
import zipfile
import kml.kmlparse
import kml.coordbox
import kml.kmz
import kml.featureset
import kml.resourcemap


class Model:

  """ API to a KMZ of a Placemark Model

  """

  def __init__(self):
    self.__name = None
    self.__kmzfile = None
    self.__kmz = None

    self.__lookat = None
    self.__latlonaltbox = None

    self.__altitudeMode = None
    self.__location = None
    self.__orientation = None
    self.__scale = None
    self.__link = None
    self.__resourcemap = None


  def SetName(self, name):
    self.__name = name

  def Name(self):
    return self.__name


  def Parse(self, kmzfile): 

    """ Parse .kmz for first Placemark/Model

    Model must have a Location and Link

    """

    kp = kml.kmlparse.KMLParse(kmzfile)
    if not self.ParseNode(kml.kmlparse.GetFirstChildElement(kp.Doc(), 'Model')):
      return False
    # If Model had no ResourceMap look for the mappings in 'textures.txt'
    if not self.__resourcemap:
      self.__resourcemap = ParseTexturesTxt(kmzfile)
    self.__kmzfile = kmzfile
    return True

  def ParseNode(self, model_node):

    """ Parse child elements of Model

    Args:
      model_node: dom node of Model

    Return:
      true: found at least Location and Link
      false: bad Model or missing Location or Link
    """

    if not model_node:
      return False

    (location_node, orientation_node, scale_node, link_node) = \
                                     kml.kmlparse.ParseModel(model_node)
    if not location_node or not link_node:
      return False

    self.__altitudeMode = kml.kmlparse.GetSimpleElementText(model_node, \
                                                            'altitudeMode')
    self.__location = kml.kmlparse.ParseLocation(location_node)
    self.__orientation = kml.kmlparse.ParseOrientation(orientation_node)
    self.__scale = kml.kmlparse.ParseScale(scale_node)
    self.__link = kml.kmlparse.ParseLink(link_node)
    resource_node_list = model_node.getElementsByTagName('ResourceMap')
    if resource_node_list:
      self.__resourcemap = kml.resourcemap.ResourceMap()
      # XXX what if there really are N?
      self.__resourcemap.ParseResourceMapNode(resource_node_list[0])
          
    return True

  def Get_altitudeMode(self):
    return self.__altitudeMode

  def Get_Location(self):
    """ kml.genxml.Location() """
    return self.__location
  
  def Get_Orientation(self):
    """ kml.genxml.Orientation() """
    return self.__orientation
  
  def Get_Scale(self):
    """ kml.genxml.Scale() """
    return self.__scale
  
  def Get_Link(self):
    """ kml.genxml.Link() """
    return self.__link

  def Get_ResourceMap(self):
    """ kml.resourcemap.ResourceMap() """
    return self.__resourcemap
  
  altitudeMode = property(fget=Get_altitudeMode)
  Location = property(fget=Get_Location)
  Orientation = property(fget=Get_Orientation)
  Scale = property(fget=Get_Scale)
  Link = property(fget=Get_Link)

  def Kmz(self):
    return self.__kmzfile


  def KmzSize(self):
    if self.__kmzfile:
      return os.path.getsize(self.__kmzfile)
    return 0


  def LonLatF(self):

    """ Model Location longitude,latitude

    Note: this is the location of the _origin_ of the model geometry...

    Returns:
      (lon,lat): float

    """

    if self.__location:
      return (float(self.__location.longitude), float(self.__location.latitude))
    else:
      return (None,None)


  def ReadFileData(self, filename):

    """ Return the contents of the given file within the KMZ

    The kmzfile must have been previously successfully Parse()'ed.

    """

    # Open the zip archive if we have not already done so
    if not self.__kmz:
      # A previous Parse() will have left a kmzfile name around
      if not self.__kmzfile:
        return None
      self.__kmz = kml.kmz.Kmz(self.__kmzfile)

    return self.__kmz.Read(filename)


  def GetGeometry(self):

    """ Return the contents of the Model's geometry file

    The geometry (Collada/dae) file is the target of the Model/Link/href.

    The kmzfile must have been previously successfully Parse()'ed

    """

    if not self.__link:
      return None
    return self.ReadFileData(self.__link.href)
    

def ParseTexturesTxt(kmzfile):
  kmz = kml.kmz.Kmz(kmzfile)
  if kmz:
    textures_txt_data = kmz.Read('textures.txt')
    if textures_txt_data:
      resourcemap = kml.resourcemap.ResourceMap()
      resourcemap.ParseTexturesTxt(textures_txt_data)
      return resourcemap
  return None


class ModelSet:

  """ A set of Models

  """

  def __init__(self, dir):
    self.__dir = dir
    # self.__models = {}
    self.__feature_set = kml.featureset.FeatureSet()

  def __iter__(self):

    """The ModelSet iterator iterates over the set of models.

    """
    self.__iter_index = 0
    return self

  def next(self):
    if self.__iter_index == self.__feature_set.Size():
      raise StopIteration
    else:
      model = self.__feature_set.GetFeature(self.__iter_index)
      self.__iter_index += 1
      return model
    
  def FindAndParse(self):
    filenames = os.listdir(self.__dir)
    for filename in filenames:
      (modelname,ext) = os.path.splitext(filename)
      if ext == '.kmz':
        model = Model()
        model.SetName(modelname)
        if model.Parse(os.path.join(self.__dir,filename)):
          (lon, lat) = model.LonLatF()
          weight = model.KmzSize() # TODO: volume-based weight
          self.__feature_set.AddWeightedFeatureAtLocation(weight, lon, lat, model)

  def FindBBOX(self):
    return self.__feature_set.NSEW()

  def FeatureSet(self):
    return self.__feature_set

  def Locations(self):
    """ List of (lon,lat,name) tuples """
    self.__feature_set.Sort()
    locations = []
    for (w,lon,lat,model) in self.__feature_set:
      locations.append((model.KmzSize(),lon,lat,model.Name()))
    return locations

  def GetModel(self, name):
    for (w,lon,lat,model) in self.__feature_set:
      if model.Name() == name:
        return model
    return None

