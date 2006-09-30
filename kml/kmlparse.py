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
import kml.genxml


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

  """DOM parse a KML file

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


  def ExtractLatLonBox(self):

    """ Returns first LatLonBox

    Returns:
      kml.genxml.LatLonBox
    """

    llbs = self.__doc.getElementsByTagName('LatLonBox')
    if not llbs:
      return None

    latlonbox = kml.genxml.LatLonBox()

    llb = llbs[0]
    north = llb.getElementsByTagName('north')
    latlonbox.north = GetText(north[0])

    south = llb.getElementsByTagName('south')
    latlonbox.south = GetText(south[0])

    east = llb.getElementsByTagName('east')
    latlonbox.east = GetText(east[0])

    west = llb.getElementsByTagName('west')
    latlonbox.west = GetText(west[0])

    return latlonbox


  def ExtractTimeSpan(self):

    """ Returns first TimeSpan

    Returns:
      kml.genxml.TimeSpan
    """

    tss = self.__doc.getElementsByTagName('TimeSpan')
    if not tss:
      return None

    timespan = kml.genxml.TimeSpan()

    ts = tss[0]
    begin = ts.getElementsByTagName('begin')
    timespan.begin = GetText(begin[0])

    end = ts.getElementsByTagName('end')
    timespan.end = GetText(end[0])

    return timespan


  def ExtractIcon(self):

    """ Returns first Icon

    Returns:
      kml.genxml.Icon
    """

    icons = self.__doc.getElementsByTagName('Icon')
    if not icons:
      return None

    icon = kml.genxml.Icon()

    i = icons[0]
    href = i.getElementsByTagName('href')
    if href:
      icon.href = GetText(href[0])

    return icon


  def ExtractGroundOverlay(self):

    """ Returns first GroundOverlay

    Returns:
      kml.genxml.GroundOverlay
    """

    gos = self.__doc.getElementsByTagName('GroundOverlay')
    if not gos:
      return None

    groundoverlay = kml.genxml.GroundOverlay()

    go = gos[0]

    drawOrder = go.getElementsByTagName('drawOrder')
    if drawOrder:
      groundoverlay.drawOrder = GetText(drawOrder[0])

    altitude = go.getElementsByTagName('altitude')
    if altitude:
      groundoverlay.altitude = GetText(altitude[0])

    altitudeMode = go.getElementsByTagName('altitudeMode')
    if altitudeMode:
      groundoverlay.altitudeMode = GetText(altitudeMode[0])
      
    return groundoverlay


  def ExtractLocation(self):

    """ Returns first Location

    Returns:
      kml.genxml.Location
    """

    locs = self.__doc.getElementsByTagName('Location')
    if not locs:
      return None

    location = kml.genxml.Location()

    loc = locs[0]

    longitude = loc.getElementsByTagName('longitude')
    if longitude:
      location.longitude = GetText(longitude[0])

    latitude = loc.getElementsByTagName('latitude')
    if latitude:
      location.latitude = GetText(latitude[0])

    altitude = loc.getElementsByTagName('altitude')
    if altitude:
      location.altitude = GetText(altitude[0])

    return location


  def ExtractOrientation(self):

    """ Returns first Orientation

    Returns:
      kml.genxml.Orientation
    """

    os = self.__doc.getElementsByTagName('Orientation')
    if not os:
      return None

    orientation = kml.genxml.Orientation()

    o = os[0]

    heading = o.getElementsByTagName('heading')
    if heading:
      orientation.heading = GetText(heading[0])

    tilt = o.getElementsByTagName('tilt')
    if tilt:
      orientation.tilt = GetText(tilt[0])

    roll = o.getElementsByTagName('roll')
    if roll:
      orientation.roll = GetText(roll[0])

    return orientation


  def ExtractScale(self):

    """ Returns first Scale

    Returns:
      kml.genxml.Scale
    """

    ss = self.__doc.getElementsByTagName('Scale')
    if not ss:
      return None

    orientation = kml.genxml.Scale()

    s = ss[0]

    x = s.getElementsByTagName('x')
    if x:
      orientation.x = GetText(x[0])

    y = s.getElementsByTagName('y')
    if y:
      orientation.y = GetText(y[0])

    z = s.getElementsByTagName('z')
    if z:
      orientation.z = GetText(z[0])

    return orientation

