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

"""KMLParse

Some utilities to parse and analyze KML

"""

import xml.dom.minidom

import kml.coordbox


def GetText(node):

  """Dig out node text

  Args:
    node: DOM node

  Returns:
    text: stripped concatenation of all TEXT_NODEs
  """

  text = []
  for child in node.childNodes:
    if child.nodeType == child.TEXT_NODE:
      text.append(child.data)
  return "".join(text).strip()


class KMLParse:

  """Manage a DOM parse a KML file

  """

  def __init__(self,kmlfile):

    self.__doc = xml.dom.minidom.parse(kmlfile)


  def Doc(self):

    return self.__doc


  def NSEW(self):

    """Return a bounding box

    Searches for all <coordinates> and sweeps out
    a bounding box enclosing them all.

    Returns:
      (n,s,e,w)
    """

    cbox = kml.coordbox.CoordBox()
    coords = self.__doc.getElementsByTagName('coordinates')
    for c in coords:
      ctext = GetText(c)
      cbox.AddCoordinates(ctext)
    return cbox.NSEW()


  def ExtractDocumentStyles(self):

    """Return <Document>'s <Style>'s and <StyleMap>'s

    Returns:
      kml - string of <Style> and <StyleMap> KML
    """

    doc = self.__doc.getElementsByTagName('Document')
    if not doc:
      return ''

    _styles = []
    for child in doc[0].childNodes:
      if child.nodeType != child.ELEMENT_NODE:
        continue
      if child.tagName == 'Style' or child.tagName == 'StyleMap':
        _styles.append(child.toxml())
    return "".join(_styles) # one KML string of all Style's and StyleMap's


  def ExtractSchemas(self):

    """Return <Document>'s <Schema>'s

    Returns:
      kml: string <Schema> KML
    """

    doc = self.__doc.getElementsByTagName('Document')
    if not doc:
      return ''
    schemas = doc[0].getElementsByTagName('Schema')
    k = []
    for schema in schemas:
      k.append(schema.toxml())
    return "".join(k)



def ParseLocation(loc):

  """Parse <Location>

  Args:
    loc: DOM node for <Location>

  Returns:
    (lon,lat): <longitude>,<latitude> as float

  """

  lat = loc.getElementsByTagName('latitude')
  if not lat:
    return ''
  lon = loc.getElementsByTagName('longitude')
  if not lon:
    return ''
  latf = float(self.GetText(lat[0]))
  lonf = float(self.GetText(lon[0]))

  return (lonf,latf)

