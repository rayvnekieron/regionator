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
import tempfile
import os

import kml.coordbox
import kml.genxml
import kml.href
import kml.kmz


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

def GetCDATA(node):
  cdata = []
  for child in node.childNodes:
    if child.nodeType == child.CDATA_SECTION_NODE:
      cdata.append(child.data)
  return "".join(cdata)

def GetSimpleElementText(node, tagname):

  """Return text of <tagname> child of node

  Args:
    node: dom node
    tagname: child element of dom node

  Returns:
    None: if node has no child of this tagname
    text: character data of <tagname>

  """

  nodelist = node.getElementsByTagName(tagname)
  if nodelist:
    return GetText(nodelist[0])
  return None


def GetFirstChildElement(node, tagname):
  if not node:
    return None
  nodelist = node.getElementsByTagName(tagname)
  if nodelist:
    return nodelist[0]
  else:
    return None


class KMLParse:

  """DOM parse a KML or KMZ file

  """

  def __init__(self,kmlfile):

    """
    Args:
      kmlfile: if .kml parse the file, if .kmz extract doc.kml and parse that
    """

    self.__doc = None
    self.__href = kml.href.Href()

    if kmlfile == None:
      return

    self.__href.SetUrl(kmlfile)
    if self.__href.GetScheme() == None:
      self._ParseFile(kmlfile)
    else:
      self._ParseHttp(kmlfile)


  def _ParseFile(self, kmlfile):
    if not kmlfile or not os.access(kmlfile, os.R_OK):
      return

    if zipfile.is_zipfile(kmlfile):
      self._ParseKMZ(kmlfile)
      return

    try:
      self.__doc = xml.dom.minidom.parse(kmlfile)
    except:
      print 'parse error'
      self.__doc = None


  def _ParseKMZ(self, kmzfile):
    kmz = kml.kmz.Kmz(kmzfile)
    if kmz:
      kmlstring = kmz.ReadKml()
      if kmlstring:
        self.ParseString(kmlstring)


  def _ParseHttp(self, kmlurl):
    tempfilename = kml.href.FetchUrlToTempFile(kmlurl)
    if tempfilename:
      self._ParseFile(tempfilename)
      os.unlink(tempfilename)


  def ParseString(self, kmlstring):
    try:
      self.__doc = xml.dom.minidom.parseString(kmlstring)
    except:
      print 'parse error'
      self.__doc = None


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

    return ParseTimeSpan(tss[0])


  def ExtractIcon(self):

    """ Returns first Icon

    Returns:
      kml.genxml.Icon
    """

    icons = self.__doc.getElementsByTagName('Icon')
    if not icons:
      return None
    return ParseIcon(icons[0])


  def ExtractLink(self):

    """ Returns first Icon

    Returns:
      kml.genxml.Link
    """

    links = self.__doc.getElementsByTagName('Link')
    if not links:
      return None
    return ParseLink(links[0])


  def ExtractGroundOverlay(self):

    """ Returns first GroundOverlay

    Returns:
      kml.genxml.GroundOverlay
    """

    gos = self.__doc.getElementsByTagName('GroundOverlay')
    if not gos:
      return None
    return ParseGroundOverlay(gos[0])


  def ExtractLocation(self):

    """ Returns first Location

    Returns:
      kml.genxml.Location
    """

    locs = self.__doc.getElementsByTagName('Location')
    if not locs:
      return None
    return ParseLocation(locs[0])


  def ExtractOrientation(self):

    """ Returns first Orientation

    Returns:
      kml.genxml.Orientation
    """

    os = self.__doc.getElementsByTagName('Orientation')
    if not os:
      return None
    return ParseOrientation(os[0])


  def ExtractScale(self):

    """ Returns first Scale

    Returns:
      kml.genxml.Scale
    """

    ss = self.__doc.getElementsByTagName('Scale')
    if not ss:
      return None
    return ParseScale(ss[0])


  def ExtractLookAt(self):

    """ Returns first LookAt

    Returns:
      kml.genxml.LookAt
    """

    las = self.__doc.getElementsByTagName('LookAt')
    if not las:
      return None
    return ParseLookAt(las[0])

  def ExtractRegion(self):

    """ Returns first Region

    Returns:
      kml.genxml.Region
    """

    region_node = GetFirstChildElement(self.__doc, 'Region')
    return ParseRegion(region_node)


def ParseLookAt(la_node):
    lookat = kml.genxml.LookAt()
    lookat.longitude = GetSimpleElementText(la_node, 'longitude')
    lookat.latitude = GetSimpleElementText(la_node, 'latitude')
    lookat.altitude = GetSimpleElementText(la_node, 'altitude')
    lookat.range = GetSimpleElementText(la_node, 'range')
    lookat.tilt = GetSimpleElementText(la_node, 'tilt')
    lookat.heading = GetSimpleElementText(la_node, 'heading')
    return lookat


def ParseLocation(loc_node):
    location = kml.genxml.Location()
    location.longitude = GetSimpleElementText(loc_node, 'longitude')
    location.latitude = GetSimpleElementText(loc_node, 'latitude')
    location.altitude = GetSimpleElementText(loc_node, 'altitude')
    return location


def ParseOrientation(o_node):
    orientation = kml.genxml.Orientation()
    orientation.heading = GetSimpleElementText(o_node, 'heading')
    orientation.tilt = GetSimpleElementText(o_node, 'tilt')
    orientation.roll = GetSimpleElementText(o_node, 'roll')
    return orientation


def ParseScale(scale_node):
    scale = kml.genxml.Scale()
    scale.x = GetSimpleElementText(scale_node, 'x')
    scale.y = GetSimpleElementText(scale_node, 'y')
    scale.z = GetSimpleElementText(scale_node, 'z')
    return scale


def ParseGroundOverlay(go_node):
    groundoverlay = kml.genxml.GroundOverlay()
    groundoverlay.drawOrder = GetSimpleElementText(go_node, 'drawOrder')
    groundoverlay.altitude = GetSimpleElementText(go_node, 'altitude')
    groundoverlay.altitudeMode = GetSimpleElementText(go_node, 'altitudeMode')
    return groundoverlay


def ParseIcon(icon_node):
    icon = kml.genxml.Icon()
    icon.href = GetSimpleElementText(icon_node, 'href')
    return icon


def ParseTimeSpan(ts_node):
    timespan = kml.genxml.TimeSpan()
    timespan.begin = GetSimpleElementText(ts_node, 'begin')
    timespan.end = GetSimpleElementText(ts_node, 'end')
    return timespan


def ParseLatLonBox(llb_node):

  """Parse <LatLonBox> dom node

  Args:
    llb_node: <LatLonBox> dom node

  Returns:
    kml.genxml.LatLonBox:
  """

  llb = kml.genxml.LatLonBox()
  GetNSEW(llb_node, llb)
  return llb


def ParseLatLonAltBox(llab_node):

  """Parse <LatLonAltBox> dom node

  Args:
    llab_node: <LatLonAltBox> dom node

  Returns:
    kml.genxml.LatLonAltBox:
  """

  llab = kml.genxml.LatLonAltBox()
  GetNSEW(llab_node, llab)
  llab.minAltitude = GetSimpleElementText(llab_node, 'minAltitude')
  llab.maxAltitude = GetSimpleElementText(llab_node, 'maxAltitude')
  llab.altitudeMode = GetSimpleElementText(llab_node, 'altitudeMode')
  return llab


def GetNSEW(node, latlonbox):

  """Parse <LatLonBox> or <LatLonAltBox> bounding box

  Parses <north>, <south>, <east>, <west> into the
  specified kml.genxml.LatLonBox

  Args:
    node: <LatLonBox> or <LatLonAltBox> dom node
    llb: kml.genxml.LatLonBox

  """

  latlonbox.north = GetSimpleElementText(node, 'north')
  latlonbox.south = GetSimpleElementText(node, 'south')
  latlonbox.east = GetSimpleElementText(node, 'east')
  latlonbox.west = GetSimpleElementText(node, 'west')


def ParseRegion(region_node):

  """Parse <Region> dom node

  Args:
    region_node: <Region> dom node

  Returns:
    (<LatLonAltBox> dom node, <Lod> dom node)
  """

  llab_node = GetFirstChildElement(region_node, 'LatLonAltBox')
  lod_node = GetFirstChildElement(region_node, 'Lod')
  return (llab_node, lod_node)


def ParseLod(lod_node):

  """Parse <Lod> dom node

  Args:
    lod_node: <Lod> dom node

  Returns:
    kml.genxml.Lod:
  """

  lod = kml.genxml.Lod()
  lod.minLodPixels = GetSimpleElementText(lod_node, 'minLodPixels')
  lod.maxLodPixels = GetSimpleElementText(lod_node, 'maxLodPixels')
  lod.minFadeExtent = GetSimpleElementText(lod_node, 'minFadeExtent')
  lod.maxFadeExtent = GetSimpleElementText(lod_node, 'maxFadeExtent')
  return lod


def ParseLink(link_node):

  """Parse <Link> dom node

  Args:
    link_node: <Link> dom node

  Returns:
    kml.genxml.Link:
  """

  link = kml.genxml.Link()
  link.href = GetSimpleElementText(link_node, 'href')
  link.viewRefreshMode = GetSimpleElementText(link_node, 'viewRefreshMode')
  return link


def ParseModel(model_node):

  """Parse <Model> dom node

  Args:
    model_node: <Model> dom node

  Returns:
    (location, orientation, scale, link): dom nodes
  """

  location_node = GetFirstChildElement(model_node, 'Location')
  orientation_node = GetFirstChildElement(model_node, 'Orientation')
  scale_node = GetFirstChildElement(model_node, 'Scale')
  link_node = GetFirstChildElement(model_node, 'Link')
  return (location_node, orientation_node, scale_node, link_node)
