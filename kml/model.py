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


import kml.kmlparse


class Model:

  """ API to a KMZ of a Placemark Model

  """

  def __init__(self):
    self.__name = None
    self.__kmzfile = None

    self.__lookat = None
    self.__latlonaltbox = None

    self.__location = None
    self.__orientation = None
    self.__scale = None
    self.__link = None


  def Parse(self, kmzfile): 

    """ Parse .kmz

    """

    kp = kml.kmlparse.KMLParse(kmzfile)
    doc = kp.Doc()
    if not doc: # parse failed
      return

    self.__kmzfile = kmzfile

    self.__location = kp.ExtractLocation() 

    self.__lookat = kp.ExtractLookAt()


  def Location(self):

    """ Model Location longitude,latitude

    Note: this is the location of the _origin_ of the model geometry...

    Returns:
      (lon,lat): float

    """

    if self.__location:
      return (float(self.__location.longitude), float(self.__location.latitude))
    else:
      return (None,None)
    

