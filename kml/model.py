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


class Model:

  """ API to a KMZ of a Placemark Model

  """

  def __init__(self):
    self.__name = None
    self.__kmzfile = None
    self.__zfd = None

    self.__lookat = None
    self.__latlonaltbox = None

    self.__altitudeMode = None
    self.__location = None
    self.__orientation = None
    self.__scale = None
    self.__link = None


  def SetName(self, name):
    self.__name = name

  def Name(self):
    return self.__name


  def Parse(self, kmzfile): 

    """ Parse .kmz for first Placemark/Model

    Model must have a Location and Link

    """

    kp = kml.kmlparse.KMLParse(kmzfile)
    doc = kp.Doc()
    if not doc: # parse failed
      return False

    nodelist = doc.getElementsByTagName('Model')
    if not nodelist:
      return False

    model_node = nodelist[0]
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
    self.__kmzfile = kmzfile

    return True

  def Get_altitudeMode(self):
    return self.__altitudeMode

  def Get_Location(self):
    return self.__location
  
  def Get_Orientation(self):
    return self.__orientation
  
  def Get_Scale(self):
    return self.__scale
  
  def Get_Link(self):
    return self.__link
  
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
    if not self.__zfd:
      # A previous Parse() will have left a kmzfile name around
      if not self.__kmzfile:
        return None
      zfd = kml.kmz.ZipOpen(self.__kmzfile)
      if not zfd:
        return None
      self.__zfd = zfd

    return self.__zfd.read(filename)


  def GetGeometry(self):

    """ Return the contents of the Model's geometry file

    The geometry (Collada/dae) file is the target of the Model/Link/href.

    The kmzfile must have been previously successfully Parse()'ed

    """

    if not self.__link:
      return None
    return self.ReadFileData(self.__link.href)
    

class ModelSet:

  """ A set of Models

  """

  def __init__(self, dir):
    self.__dir = dir
    self.__models = {}

  def __iter__(self):

    """The ModelSet iterator iterates over the set of model.

    """

    # The .next() of this iterator returns a kml.model.Model
    return self.__models.itervalues()

  def FindAndParse(self):
    filenames = os.listdir(self.__dir)
    for filename in filenames:
      (modelname,ext) = os.path.splitext(filename)
      if ext == '.kmz':
        model = Model()
        model.SetName(modelname)
        if model.Parse(os.path.join(self.__dir,filename)):
          self.__models[modelname] = model

  def FindBBOX(self):
    self.__cbox = kml.coordbox.CoordBox()
    for modelname in self.__models:
      model = self.__models[modelname]
      (lon,lat) = model.LonLatF()
      self.__cbox.AddPoint(lon,lat)
    return self.__cbox.NSEW()

  def Locations(self):
    """ List of (lon,lat,name) tuples """
    locations = []
    for modelname in self.__models:
      model = self.__models[modelname]
      (lon,lat) = model.LonLatF()
      name = model.Name()
      # dsu - decordate
      locations.append((model.KmzSize(),lon,lat,name))
    # dsu - sort
    locations.sort()
    locations.reverse()
    # dsu - undecorate
    return_locations = []
    for loc in locations:
      return_locations.append((loc[1],loc[2],loc[3]))
    return return_locations

  def GetModel(self, name):
    if self.__models.has_key(name):
      return self.__models[name]
    return None

