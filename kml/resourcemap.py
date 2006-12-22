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


class ResourceMapItem:

  """ 
  This maps a resource in a geometry (Collada) file to a (kmz) file name
  """

  def __init__(self):

    self.__geom_path = None
    self.__kmz_path = None
    self.__model_id = None


  def ParseTexturesTxtLine(self, line):

    """Set this item from a line in textures.txt format:

    Args:
      line: <geom_path> <kmz_path> [<model_id>]

    """
    item = line.split('>')
    num_words = len(item)
    if num_words < 3 or num_words > 4:
      return False
    self.__geom_path = item[0].strip().strip('<').strip()
    self.__kmz_path = item[1].strip().strip('<').strip()
    if num_words == 4:
      self.__model_id = item[2].strip().strip('<').strip()
    return True


  def Mapping(self):

    """Return the mapping item as a tuple

    Returns:
      (geom_path, kmz_path, model_id)
    """

    return (self.__geom_path, self.__kmz_path, self.__model_id)



class ResourceMap:

  """This is a set of ResourceMapItems

  This is represents the data in a model.kmz's textures.txt

  """

  def __init__(self):
    self.__items = [] # list of ResourceMapItem's
    self.__geom_map = {} # map geom_path to RMI
    self.__kmz_map = {} # map kmz_path to RMI

  def __iter__(self):
    self.__iter_index = 0
    return self

  def next(self):
    if self.__iter_index > len(self.__items) - 1:
      raise StopIteration
    item = self.__items[self.__iter_index]
    self.__iter_index += 1
    return item

  def Size(self):

    """ Returns the number of ResourceMapItems """

    return len(self.__items)

  def ParseTexturesTxt(self, textures_txt_data):

    """Set mapping state from a textures.txt file

    Args:
      textures_txt_data: contents of textures.txt file
    """

    for line in textures_txt_data.split('\n'):
      item = ResourceMapItem()
      if item.ParseTexturesTxtLine(line):
        self.__items.append(item)
        (geom_path, kmz_path, model_id) = item.Mapping()
        self.__geom_map[geom_path] = item
        self.__kmz_map[kmz_path] = item

  def LookupByGeomPath(self, geom_path):

    """Lookup ResourceMapItem by geometry path

    Args:
      geom_path: geometry path

    Returns:
      kml.resourcemap.ResourceMapItem:
    """

    if self.__geom_map.has_key(geom_path):
      return self.__geom_map[geom_path]
    return None

  def GetKmzPath(self, geom_path):

    """Map geometry path to kmz path

    Args:
      geom_path: geometry path

    Returns:
      kmz_path: kmz path
    """

    rmi = self.LookupByGeomPath(geom_path)
    if rmi:
      (gp,kp,mid) = rmi.Mapping()
      return kp
    return None

  def LookupByKmzPath(self, kmz_path):

    """Lookup ResourceMapItem by kmz path

    Args:
      kmz_path: kmz path

    Returns:
      kml.resourcemap.ResourceMapItem:
    """

    if self.__kmz_map.has_key(kmz_path):
      return self.__kmz_map[kmz_path]
    return None

  def GetGeomPath(self, kmz_path):

    """Map kmz path to geometry path

    Args:
      kmz_path: kmz path

    Returns:
      geom_path: geometry path
    """

    rmi = self.LookupByKmzPath(kmz_path)
    if rmi:
      (gp,kp,mid) = rmi.Mapping()
      return gp
    return None
