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
import zipfile

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

  """DOM parse a KML or KMZ file

  """

  def __init__(self,kmlfile):

    """
    Args:
      kmlfile: if .kml parse the file, if .kmz extract doc.kml and parse that
    """

    self.__doc = None
    if kmlfile == None:
      return

    if zipfile.is_zipfile(kmlfile):
      self.ParseKMZ(kmlfile)
      return

    self.__doc = xml.dom.minidom.parse(kmlfile)


  def ParseKMZ(self, kmzfile):
    z = zipfile.ZipFile(kmzfile)
    for name in z.namelist():
      if name.endswith('.kml'): # GE reads first .kml in the archive
        kmlstring = z.read(name)
        self.__doc = xml.dom.minidom.parseString(kmlstring)


  def ParseString(self, kmlstring):
    self.__doc = xml.dom.minidom.parseString(kmlstring)


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

    return ParseLatLonBox(llbs[0])


  def ExtractLatLonAltBox(self):

    """ Returns first LatLonAltBox

    Returns:
      kml.genxml.LatLonAltBox
    """

    llabs = self.__doc.getElementsByTagName('LatLonAltBox')
    if not llabs:
      return None

    return ParseLatLonAltBox(llabs[0])


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


  def ExtractLink(self):

    """ Returns first Icon

    Returns:
      kml.genxml.Link
    """

    links = self.__doc.getElementsByTagName('Link')
    if not links:
      return None

    link = kml.genxml.Link()

    l = links[0]
    href = l.getElementsByTagName('href')
    if href:
      link.href = GetText(href[0])

    return link


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


  def ExtractLookAt(self):

    """ Returns first LookAt

    Returns:
      kml.genxml.LookAt
    """

    las = self.__doc.getElementsByTagName('LookAt')
    if not las:
      return None

    lookat = kml.genxml.LookAt()

    la = las[0]

    longitude = la.getElementsByTagName('longitude')
    if longitude:
      lookat.longitude = GetText(longitude[0])

    latitude = la.getElementsByTagName('latitude')
    if latitude:
      lookat.latitude = GetText(latitude[0])

    altitude = la.getElementsByTagName('altitude')
    if altitude:
      lookat.altitude = GetText(altitude[0])

    range = la.getElementsByTagName('range')
    if range:
      lookat.range = GetText(range[0])

    tilt = la.getElementsByTagName('tilt')
    if tilt:
      lookat.tilt = GetText(tilt[0])

    heading = la.getElementsByTagName('heading')
    if heading:
      lookat.heading = GetText(heading[0])

    return lookat


def ParseLatLonBox(node):
  llab = kml.genxml.LatLonAltBox()
  GetNSEW(node, llab)
  return llab


def ParseLatLonAltBox(llab_node):

  llab = kml.genxml.LatLonAltBox()

  GetNSEW(llab_node, llab)

  minAltitude = llab_node.getElementsByTagName('minAltitude')
  if minAltitude:
    llab.minAltitude = GetText(minAltitude[0])

  maxAltitude = llab_node.getElementsByTagName('maxAltitude')
  if maxAltitude:
    llab.maxAltitude = GetText(maxAltitude[0])

  altitudeMode = llab_node.getElementsByTagName('altitudeMode')
  if altitudeMode:
    llab.altitudeMode = GetText(altitudeMode[0])

  return llab


def GetNSEW(node, latlonbox):

  north = node.getElementsByTagName('north')
  if north:
    latlonbox.north = GetText(north[0])

  south = node.getElementsByTagName('south')
  if south:
    latlonbox.south = GetText(south[0])

  east = node.getElementsByTagName('east')
  if east:
    latlonbox.east = GetText(east[0])

  west = node.getElementsByTagName('west')
  if west:
    latlonbox.west = GetText(west[0])


def ParseRegion(region_node):

  llab_node = None
  llab_list = region_node.getElementsByTagName('LatLonAltBox')
  if llab_list:
    llab_node = llab_list[0]

  lod_node = None
  lod_list = region_node.getElementsByTagName('Lod')
  if lod_list:
    lod_node = lod_list[0]
  return (llab_node, lod_node)


def ParseLod(lod_node):

  lod = kml.genxml.Lod()

  n = lod_node.getElementsByTagName('minLodPixels')
  if n:
    lod.minLodPixels = GetText(n[0])

  n = lod_node.getElementsByTagName('maxLodPixels')
  if n:
    lod.maxLodPixels = GetText(n[0])

  n = lod_node.getElementsByTagName('minFadeExtent')
  if n:
    lod.minFadeExtent = GetText(n[0])

  n = lod_node.getElementsByTagName('maxFadeExtent')
  if n:
    lod.maxFadeExtent = GetText(n[0])

  return lod


def ParseLink(link_node):

  link = kml.genxml.Link()

  href = link_node.getElementsByTagName('href')
  if href:
    link.href = GetText(href[0])

  vfr = link_node.getElementsByTagName('viewRefreshMode')
  if vfr:
    link.viewRefreshMode = GetText(vfr[0])

  return link


