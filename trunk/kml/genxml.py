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

import kml.version


def SimpleElement(tag, value):

  """
  Args:
    tag: xml tag name
    value: character data

  Returns:
    XML: <tag>value</tag>
  """

  return '<%s>%s</%s>\n' % (tag, value, tag)


def SimpleElementList(elements):

  """
  Args:
    elements: list of element name value string pair tuples

  Returns:
    XML: <tag>value</tag>...
  """

  el = []
  for pair in elements:
    el.append(SimpleElement(pair[0],pair[1]))
  return "".join(el)


def ElementAttributes(attributes):

  """
  Pretty much assumes one or more attr/val pairs.

  Args:
    attributes: list of (attrname, attrval) tuples

  Returns:
   string: xml formatted string attr="attrval"...
  """

  attrs = []
  for pair in attributes:
      attrs.append(' ')
      attrs.append('%s=\"%s\"' % (pair[0],pair[1]))
  return "".join(attrs)


def ComplexElement(tag, attributes, comment, elements, children):

  """Create XML for a complex element

  'elements' is a list of simple child elements.
  'children' is the xml of all complex child elements of this tag.

  Args:
    tag: tag name
    attributes: list of name,value string pairs
    comment: xml comment string
    elements: list of name,value string pairs
    children: xml string of child elements

  Returns:
   XML: <tag [attributes]>[comment][elements][children]</tag>
  """

  xml = []
  xml.append('<%s' % tag)
  if attributes:
    xml.append(ElementAttributes(attributes))
  if elements or children or comment:
    xml.append('>\n')
    if comment:
      xml.append(comment)
    if elements:
      xml.append(SimpleElementList(elements))
    if children:
      xml.append(children)
    xml.append('</%s>\n' % tag)
  else:
    xml.append('/>\n')
  return "".join(xml)


class Kml(object):

  """ <kml>[comment][<NetworkLinkControl>][Feature]</kml>
  """

  def __init__(self):
    self.__comment = None
    self.__NetworkLinkControl = None
    self.__Feature = None

  def Set_comment(self, comment):
    self.__comment = comment

  def Set_NetworkLinkControl(self, nlc):
    self.__NetworkLinkControl = nlc

  def Set_Feature(self, f):
    self.__Feature = f

  comment = property(fset=Set_comment)
  Feature = property(fset=Set_Feature)
  NetworkLinkControl = property(fset=Set_NetworkLinkControl)

  def xml(self):
    al = [('xmlns','http://earth.google.com/kml/2.1')]
    comment = self.__comment
    children = []
    if self.__NetworkLinkControl:
      children.append(self.__NetworkLinkControl)
    if self.__Feature:
      children.append(self.__Feature)
    kstr = ComplexElement('kml', al, comment, None, "".join(children))
    xmlheader = '<?xml version="1.0" encoding="UTF-8"?>'
    comment = '<!-- KML Regionator %s -->' % kml.version.Revision()
    return "\n".join((xmlheader, comment, kstr))


class Object(object):

  def __init__(self):
    self.__id = None
    self.__targetId = None

  def Set_id(self,id):
    self.__id = id

  def Set_targetId(self,id):
    self.__targetId = id

  id = property(fset=Set_id)
  targetId = property(fset=Set_targetId)

  def attributes(self):
    al = []
    if self.__id:
      al.append(('id',self.__id))
    if self.__targetId:
      al.append(('targetId',self.__targetId))
    return al

  def elements(self):
    return []


class Feature(Object):

  def __init__(self):
    Object.__init__(self)

    self.__name = None
    self.__visibility = None
    self.__open = None
    self.__address = None
    self.__AddressDetails = None
    self.__phoneNumber = None
    self.__Snippet = None
    self.__description = None
    self.__AbstractView = None
    self.__TimePrimitive = None
    self.__styleUrl = None
    self.__StyleSelectorList = []
    self.__Region = None

  def Set_name(self,name):
    self.__name = name

  def Set_visibility(self,visibility):
    self.__visibility = visibility

  def Set_open(self,open):
    self.__open = open

  def Set_Snippet(self, Snippet):
    self.__Snippet = Snippet

  def Set_description(self, description):
    self.__description = description

  def Set_AbstractView(self, l):
    self.__AbstractView = l

  def Set_TimePrimitive(self, t):
    self.__TimePrimitive = t

  def Set_styleUrl(self,styleUrl):
    self.__styleUrl = SimpleElement('styleUrl', styleUrl)

  def Add_Style(self, s):
    self.__StyleSelectorList.append(s)

  def Set_Region(self,region):
    self.__Region = region

  name = property(fset=Set_name)
  visibility = property(fset=Set_visibility)
  open = property(fset=Set_open)
  Snippet = property(fset=Set_Snippet)
  description = property(fset=Set_description)
  AbstractView = property(fset=Set_AbstractView)
  TimePrimitive = property(fset=Set_TimePrimitive)
  styleUrl = property(fset=Set_styleUrl)
  Region = property(fset=Set_Region)

  def attributes(self):
    return Object.attributes(self)

  def elements(self):
    el = Object.elements(self)
    if self.__name:
      el.append(('name',self.__name))
    if self.__visibility:
      el.append(('visibility',self.__visibility))
    if self.__open:
      el.append(('open',self.__open))
    if self.__Snippet:
      el.append(('Snippet',self.__Snippet))
    if self.__description:
      el.append(('description',self.__description))
    return el

  def children(self):
    children = []
    if self.__AbstractView:
      children.append(self.__AbstractView)
    if self.__TimePrimitive:
      children.append(self.__TimePrimitive)
    if self.__styleUrl:
      children.append(self.__styleUrl)
    for s in self.__StyleSelectorList:
      children.append(s)
    if self.__Region:
      children.append(self.__Region)
    return children


class Container(Feature):

  def __init__(self):
    Feature.__init__(self)

  def attributes(self):
    return Feature.attributes(self)

  def elements(self):
    return Feature.elements(self)

  def children(self):
    return Feature.children(self)


class Document(Container):

  """<Document>...</Document>
  """

  def __init__(self):
    Container.__init__(self)
    self.__SchemaList = []
    self.__FeatureList = []

  def attributes(self):
    return Container.attributes(self)

  def elements(self):
    return Container.elements(self)

  def children(self):
    return Container.children(self)

  def Add_Schema(self, f):
    self.__SchemaList.append(f)

  def Add_Feature(self, f):
    self.__FeatureList.append(f)

  def xml(self):
    """
    """
    al = self.attributes()
    el = self.elements()
    children = self.children()
    for s in self.__SchemaList:
      children.append(s)
    for f in self.__FeatureList:
      children.append(f)
    return ComplexElement('Document', al, None, el, "".join(children))


class Folder(Container):

  """<Folder>...</Folder>
  """

  def __init__(self):
    Container.__init__(self)
    self.__FeatureList = []

  def attributes(self):
    return Container.attributes(self)

  def elements(self):
    return Container.elements(self)

  def children(self):
    return Container.children(self)

  def Add_Feature(self, f):
    self.__FeatureList.append(f)

  def xml(self):
    """
    """
    al = self.attributes()
    el = self.elements()
    children = self.children()
    for f in self.__FeatureList:
      children.append(f)
    return ComplexElement('Folder', al, None, el, "".join(children))


class NetworkLink(Feature):

  """<NetworkLink>...</NetworkLink>
  """

  def __init__(self):
    Feature.__init__(self)
    self.__Link = None

  def Set_Link(self, link):
    self.__Link = link

  Link = property(fset=Set_Link)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = self.children()
    if self.__Link:
      children.append(self.__Link)
    return ComplexElement('NetworkLink', al, None, el, "".join(children))


class Link(Object):

  """<Link>...</Link>
  """

  def __init__(self):
    Object.__init__(self)
    self.__href = None
    self.__viewRefreshMode = None
    self.__viewRefreshTime = None
    self.__viewFormat = None

  def Set_href(self, href):
    self.__href = href

  def Get_href(self):
    return self.__href

  def Set_viewRefreshMode(self, viewRefreshMode):
    self.__viewRefreshMode = viewRefreshMode

  def Get_viewRefreshMode(self):
    return self.__viewRefreshMode

  def Set_viewRefreshTime(self, viewRefreshTime):
    self.__viewRefreshTime = viewRefreshTime

  def Set_viewFormat(self, viewFormat):
    self.__viewFormat = viewFormat

  href = property(fset=Set_href, fget=Get_href)
  viewRefreshMode = property(fset=Set_viewRefreshMode, fget=Get_viewRefreshMode)
  viewRefreshTime = property(fset=Set_viewRefreshTime)
  viewFormat = property(fset=Set_viewFormat)

  def elements(self):
    el = Object.elements(self)
    if self.__href:
      el.append(('href',self.__href))
    if self.__viewRefreshMode:
      el.append(('viewRefreshMode',self.__viewRefreshMode))
    if self.__viewRefreshTime:
      el.append(('viewRefreshTime',self.__viewRefreshTime))
    if self.__viewFormat:
      el.append(('viewFormat',self.__viewFormat))
    return el

  def children(self):
    children = []
    # hack to generate an empty <viewFormat/> if no viewFormat params specified
    if not self.__viewFormat:
      children.append(ComplexElement('viewFormat', None, None, None, None))
    return "".join(children)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = self.children()
    return ComplexElement('Link', al, None, el, children)


class Icon(Link):

  """<Icon>...</Icon>
  """

  def __init__(self):
    Link.__init__(self)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('Icon', al, None, el, None)


class Placemark(Feature):

  """<Placemark>...</Placemark>
  """

  def __init__(self):
    Feature.__init__(self)
    self.__geometry = None
    
  def Set_Geometry(self,geometry):
    self.__geometry = geometry
  
  Geometry = property(fset=Set_Geometry)

  def children(self):
    children = Feature.children(self)
    if self.__geometry:
      children.append(self.__geometry)
    return "".join(children)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = self.children()
    return ComplexElement('Placemark', al, None, el, children)




class LatLonBox(Object):

  """<LatLonBox>...</LatLonBox>
  """

  def __init__(self):
    self.__north = None
    self.__south = None
    self.__east = None
    self.__west = None
    self.__rotation = None

  def Set_NSEW(self,n,s,e,w):

    """ Set bounds as floats """

    self.__north = repr(n)
    self.__south = repr(s)
    self.__east = repr(e)
    self.__west = repr(w)

  def Get_NSEW(self):
    return (self.__north, self.__south, self.__east, self.__west)

  def Set_north(self, north):
    """ string """
    self.__north = north

  def Get_north(self):
    """ string """
    return self.__north

  def Set_south(self, south):
    """ string """
    self.__south = south

  def Get_south(self):
    """ string """
    return self.__south

  def Set_east(self, east):
    """ string """
    self.__east = east

  def Get_east(self):
    """ string """
    return self.__east

  def Set_west(self, west):
    """ string """
    self.__west = west

  def Get_west(self):
    """ string """
    return self.__west

  north = property(fset=Set_north,fget=Get_north)
  south = property(fset=Set_south,fget=Get_south)
  east = property(fset=Set_east,fget=Get_east)
  west = property(fset=Set_west,fget=Get_west)

  def elements(self):
    el = Object.elements(self)
    if self.__north:
      el.append(('north',self.__north))
    if self.__south:
      el.append(('south',self.__south))
    if self.__east:
      el.append(('east',self.__east))
    if self.__west:
      el.append(('west',self.__west))
    if self.__rotation:
      el.append(('rotation',self.__rotation))
    return el

  def xml(self):
    el = self.elements()
    return ComplexElement('LatLonBox', None, None, el, None)


class LatLonAltBox(LatLonBox):

  """<LatLonAltBox>...</LatLonAltBox>
  """

  def __init__(self):
    LatLonBox.__init__(self)
    self.__minAltitude = None
    self.__maxAltitude = None
    self.__altitudeMode = None

  def Set_minAltitude(self, minAltitude):
    self.__minAltitude = minAltitude

  def Get_minAltitude(self):
    return self.__minAltitude

  def Set_maxAltitude(self, maxAltitude):
    self.__maxAltitude = maxAltitude

  def Get_maxAltitude(self):
    return self.__maxAltitude

  def Set_altitudeMode(self, altitudeMode):
    self.__altitudeMode = altitudeMode

  def Get_altitudeMode(self):
    return self.__altitudeMode

  minAltitude = property(fset=Set_minAltitude, fget=Get_minAltitude)
  maxAltitude = property(fset=Set_maxAltitude, fget=Get_maxAltitude)
  altitudeMode = property(fset=Set_altitudeMode, fget=Get_altitudeMode)

  def elements(self):
    el = LatLonBox.elements(self)
    if self.__minAltitude:
      el.append(('minAltitude',self.__minAltitude))
    if self.__maxAltitude:
      el.append(('maxAltitude',self.__maxAltitude))
    if self.__altitudeMode:
      el.append(('altitudeMode',self.__altitudeMode))
    return el

  def xml(self):
    el = self.elements()
    return ComplexElement('LatLonAltBox', None, None, el, None)


class Lod(Object):

  """<Lod>...</Lod>
  """

  def __init__(self):
    Object.__init__(self)
    self.__minlodpixels = None
    self.__maxlodpixels = None
    self.__minfadeextent = None
    self.__maxfadeextent = None

  def Set_minLodPixels(self, minlodpixels):
    self.__minlodpixels = minlodpixels

  def Get_minLodPixels(self):
    return self.__minlodpixels

  def Set_maxLodPixels(self, maxlodpixels):
    self.__maxlodpixels = maxlodpixels

  def Get_maxLodPixels(self):
    return self.__maxlodpixels

  def Set_minFadeExtent(self, minfadeextent):
    self.__minfadeextent = minfadeextent

  def Get_minFadeExtent(self):
    return self.__minfadeextent

  def Set_maxFadeExtent(self, maxfadeextent):
    self.__maxfadeextent = maxfadeextent

  def Get_maxFadeExtent(self):
    return self.__maxfadeextent

  minLodPixels = property(fset=Set_minLodPixels, fget=Get_minLodPixels)
  maxLodPixels = property(fset=Set_maxLodPixels, fget=Get_maxLodPixels)
  minFadeExtent = property(fset=Set_minFadeExtent, fget=Get_minFadeExtent)
  maxFadeExtent = property(fset=Set_maxFadeExtent, fget=Get_maxFadeExtent)

  def elements(self):
    el = Object.elements(self)
    if self.__minlodpixels:
      el.append(('minLodPixels',self.__minlodpixels))
    if self.__maxlodpixels:
      el.append(('maxLodPixels',self.__maxlodpixels))
    if self.__minfadeextent:
      el.append(('minFadeExtent',self.__minfadeextent))
    if self.__maxfadeextent:
      el.append(('maxFadeExtent',self.__maxfadeextent))
    return el

  def xml(self):
    el = self.elements()
    return ComplexElement('Lod', None, None, el, None)


class Region(Object):

  """<Region>...</Region>
  """

  def __init__(self):
    Object.__init__(self)
    self.__latlonaltbox = None
    self.__lod = None

  def Set_Lod(self, lod):
    self.__lod = lod

  def Set_LatLonAltBox(self, latlonaltbox):
    self.__latlonaltbox = latlonaltbox

  Lod = property(fset=Set_Lod)
  LatLonAltBox = property(fset=Set_LatLonAltBox)

  def xml(self):
    al = self.attributes()
    children = []
    if self.__lod:
      children.append(self.__lod)
    if self.__latlonaltbox:
      children.append(self.__latlonaltbox)
    return ComplexElement('Region', al, None, None, "".join(children))


class Geometry(Object):

  def __init__(self):
    Object.__init__(self)
    self.__extrude = None
    self.__tessellate = None
    self.__altitudeMode = None

  def attributes(self):
    return Object.attributes(self)

  def elements(self):
    el = Object.elements(self)
    if self.__extrude:
      el.append(('extrude',self.__extrude))
    if self.__tessellate:
      el.append(('tessellate',self.__tessellate))
    if self.__altitudeMode:
      el.append(('altitudeMode',self.__altitudeMode))
    return el

  def Set_extrude(self, extrude):
    self.__extrude = extrude

  def Set_tessellate(self, tessellate):
    self.__tessellate = tessellate

  def Set_altitudeMode(self, altitudeMode):
    self.__altitudeMode = altitudeMode

  extrude = property(fset=Set_extrude)
  tessellate = property(fset=Set_tessellate)
  altitudeMode = property(fset=Set_altitudeMode)


class Point(Geometry):

  """<Point>...</Point>
  """

  def __init__(self):
    Geometry.__init__(self)
    self.__coordinates = None

  def Set_coordinates(self, coordinates):
    self.__coordinates = coordinates

  coordinates = property(fset=Set_coordinates)

  def elements(self):
    el = Geometry.elements(self)
    if self.__coordinates:
      el.append(('coordinates',self.__coordinates))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('Point', al, None, el, None)


class LineString(Geometry):

  """<LineString>...</LineString>
  """

  def __init__(self):
    Geometry.__init__(self)
    self.__coordinates = None

  def Set_coordinates(self, coordinates):
    self.__coordinates = coordinates

  coordinates = property(fset=Set_coordinates)

  def elements(self):
    el = Geometry.elements(self)
    if self.__coordinates:
      el.append(('coordinates',self.__coordinates))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('LineString', al, None, el, None)


class LinearRing(Geometry):

  """<LinearRing>...</LinearRing>
  """

  def __init__(self):
    Geometry.__init__(self)
    self.__coordinates = None

  def Set_coordinates(self, coordinates):
    self.__coordinates = coordinates

  coordinates = property(fset=Set_coordinates)

  def elements(self):
    el = Geometry.elements(self)
    if self.__coordinates:
      el.append(('coordinates',self.__coordinates))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('LinearRing', al, None, el, None)


class MultiGeometry(Geometry):

  def __init__(self):
    Geometry.__init__(self)
    self.__GeometryList = []

  def AddGeometry(self, geometry_xml):
    self.__GeometryList.append(geometry_xml)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = []
    for f in self.__GeometryList:
      children.append(f)
    return ComplexElement('MultiGeometry', al, None, el, "".join(children))


class Boundary(object):

  def __init__(self):
    self._linearring = None

  def Set_LinearRing(self, linearring):
    self._linearring = linearring # "protected"

  LinearRing = property(fset=Set_LinearRing)


class outerBoundaryIs(Boundary):

  """<outerBoundaryIs>...</outerBoundaryIs>
  """

  def __init__(self):
    Boundary.__init__(self)

  def xml(self):
    return ComplexElement('outerBoundaryIs', None, None, None, self._linearring)


class innerBoundaryIs(Boundary):

  """<innerBoundaryIs>...</innerBoundaryIs>
  """

  def __init__(self):
    Boundary.__init__(self)

  def xml(self):
    return ComplexElement('innerBoundaryIs', None, None, None, self._linearring)


class Polygon(Geometry):

  """<Polygon>...</Polygon>
  """

  def __init__(self):
    Geometry.__init__(self)
    self.__outerBoundaryIs = None
    self.__innerBoundaryIs = None

  def Set_outerBoundaryIs(self, outer):
    self.__outerBoundaryIs = outer

  def Set_innerBoundaryIs(self, inner):
    self.__innerBoundaryIs = inner

  outerBoundaryIs = property(fset=Set_outerBoundaryIs)
  innerBoundaryIs = property(fset=Set_innerBoundaryIs)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = []
    if self.__outerBoundaryIs:
      children.append(self.__outerBoundaryIs)
    if self.__innerBoundaryIs:
      children.append(self.__innerBoundaryIs)
    return ComplexElement('Polygon', al, None, el, "".join(children))


class AbstractView(Object):

  """Elements common to LookAt and Camera
  """

  def __init__(self):
    Object.__init__(self)
    self.__longitude = None
    self.__latitude = None
    self.__altitude = None
    self.__tilt = None
    self.__heading = None
    self.__altitudeMode = None

  def Set_longitude(self, longitude):
    self.__longitude = longitude

  def Get_longitude(self):
    return self.__longitude

  def Set_latitude(self, latitude):
    self.__latitude = latitude

  def Get_latitude(self):
    return self.__latitude

  def Set_altitude(self, altitude):
    self.__altitude = altitude

  def Get_altitude(self):
    return self.__altitude

  def Set_tilt(self, tilt):
    self.__tilt = tilt

  def Get_tilt(self):
    return self.__tilt

  def Set_heading(self, heading):
    self.__heading = heading

  def Get_heading(self):
    return self.__heading

  def Set_altitudeMode(self, altitudeMode):
    self.__altitudeMode = altitudeMode

  def Get_altitudeMode(self):
    return self.__altitudeMode

  longitude = property(fset=Set_longitude, fget=Get_longitude)
  latitude = property(fset=Set_latitude, fget=Get_latitude)
  altitude = property(fset=Set_altitude, fget=Get_altitude)
  tilt = property(fset=Set_tilt, fget=Get_tilt)
  heading = property(fset=Set_heading, fget=Get_heading)
  altitudeMode = property(fset=Set_altitudeMode, fget=Get_altitudeMode)

  def elements(self):
    el = Object.elements(self)
    if self.__longitude:
      el.append(('longitude',self.__longitude))
    if self.__latitude:
      el.append(('latitude',self.__latitude))
    if self.__altitude:
      el.append(('altitude',self.__altitude))
    if self.__tilt:
      el.append(('tilt',self.__tilt))
    if self.__heading:
      el.append(('heading',self.__heading))
    if self.__altitudeMode:
      el.append(('altitudeMode',self.__altitudeMode))
    return el


class LookAt(AbstractView):
  def __init__(self):
    AbstractView.__init__(self)
    self.__range = None

  def Set_range(self, range):
    self.__range = range

  def Get_range(self):
    return self.__range

  range = property(fset=Set_range, fget=Get_range)

  def elements(self):
    el = AbstractView.elements(self)
    if self.__range:
      el.append(('range',self.__range))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('LookAt', al, None, el, None)


class Camera(AbstractView):
  def __init__(self):
    AbstractView.__init__(self)
    self.__roll = None

  def Set_roll(self, roll):
    self.__roll = roll

  def Get_roll(self):
    return self.__roll

  roll = property(fset=Set_roll, fget=Get_roll)

  def elements(self):
    el = AbstractView.elements(self)
    if self.__roll:
      el.append(('roll',self.__roll))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('Camera', al, None, el, None)


class NetworkLinkControl(object):

  def __init__(self):
    self.__minRefreshPeriod = None
    self.__cookie = None
    self.__message = None
    self.__linkName = None
    self.__linkDescription = None
    self.__linkSnippet = None
    self.__expires = None
    self.__Update = None
    self.__LookAt = None

  def Set_minRefreshPeriod(self, minRefreshPeriod):
    self.__minRefreshPeriod = minRefreshPeriod

  def Set_cookie(self, cookie):
    self.__cookie = cookie

  def Set_message(self, message):
    self.__message = message

  def Set_linkName(self, linkName):
    self.__linkName = linkName

  def Set_linkDescription(self, linkDescription):
    self.__linkDescription = linkDescription

  def Set_linkSnippet(self, linkSnippet):
    self.__linkSnippet = linkSnippet

  def Set_expires(self, expires):
    self.__expires = expires

  def Set_Update(self, Update):
    self.__Update = Update

  def Set_LookAt(self, LookAt):
    self.__LookAt = LookAt

  minRefreshPeriod = property(fset=Set_minRefreshPeriod)
  cookie = property(fset=Set_cookie)
  message = property(fset=Set_message)
  linkName = property(fset=Set_linkName)
  linkDescription = property(fset=Set_linkDescription)
  linkSnippet = property(fset=Set_linkSnippet)
  expires = property(fset=Set_expires)
  Update = property(fset=Set_Update)
  LookAt = property(fset=Set_LookAt)

  def elements(self):
    el = []
    if self.__minRefreshPeriod:
      el.append(('minRefreshPeriod',self.__minRefreshPeriod))
    if self.__cookie:
      el.append(('cookie',self.__cookie))
    if self.__message:
      el.append(('message',self.__message))
    if self.__linkName:
      el.append(('linkName',self.__linkName))
    if self.__linkDescription:
      el.append(('linkDescription',self.__linkDescription))
    if self.__linkSnippet:
      el.append(('linkSnippet',self.__linkSnippet))
    if self.__expires:
      el.append(('expires',self.__expires))
    return el

  def children(self):
    children = []
    if self.__Update:
      children.append(self.__Update)
    if self.__LookAt:
      children.append(self.__LookAt)
    return "".join(children)

  def xml(self):
    el = self.elements()
    children = self.children()
    return ComplexElement('NetworkLinkControl', None, None, el, children)


class Overlay(Feature):

  def __init__(self):
    Feature.__init__(self)
    self.__color = None
    self.__drawOrder = None
    self.__Icon = None

  def Set_color(self, color):
    self.__color = color

  def Set_drawOrder(self, drawOrder):
    self.__drawOrder = drawOrder

  def Get_drawOrder(self):
    return self.__drawOrder

  def Set_Icon(self, Icon):
    self.__Icon = Icon

  color = property(fset=Set_color)
  drawOrder = property(fset=Set_drawOrder, fget=Get_drawOrder)
  Icon = property(fset=Set_Icon)

  def elements(self):
    el = Feature.elements(self)
    if self.__color:
      el.append(('color',self.__color))
    if self.__drawOrder:
      el.append(('drawOrder',self.__drawOrder))
    return el

  def children(self):
    children = Feature.children(self)
    if self.__Icon:
      children.append(self.__Icon)
    return children


class GroundOverlay(Overlay):

  def __init__(self):
    Overlay.__init__(self)
    self.__latlonbox = None
    self.__altitude = None
    self.__altitudeMode = None

  def Set_LatLonBox(self, latlonbox):
    self.__latlonbox = latlonbox

  def Set_altitude(self, altitude):
    self.__altitude = altitude

  def Get_altitude(self):
    return self.__altitude

  def Set_altitudeMode(self, altitudeMode):
    self.__altitudeMode = altitudeMode

  def Get_altitudeMode(self):
    return self.__altitudeMode

  LatLonBox = property(fset=Set_LatLonBox)
  altitude = property(fset=Set_altitude,fget=Get_altitude)
  altitudeMode = property(fset=Set_altitudeMode,fget=Get_altitudeMode)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    # XXX ordering...
    if self.__altitude:
      el.append(('altitude',self.__altitude))
    if self.__altitudeMode:
      el.append(('altitudeMode',self.__altitudeMode))
    children = Overlay.children(self)
    if self.__latlonbox:
      children.append(self.__latlonbox)
    return ComplexElement('GroundOverlay', al, None, el, "".join(children))


class vec2Type(object):

  def __init__(self):
    self.__x = 0
    self.__y = 0
    self.__xunits = None
    self.__yunits = None

  def Set_x(self, x):
    self.__x = x

  def Set_y(self, y):
    self.__y = y

  def Set_xunits(self, xunits):
    self.__xunits = xunits

  def Set_yunits(self, yunits):
    self.__yunits = yunits

  x = property(fset=Set_x)
  y = property(fset=Set_y)
  xunits = property(fset=Set_xunits)
  yunits = property(fset=Set_yunits)

  def attributes(self):
    al = []
    if self.__x:
      al.append(('x',self.__x))
    if self.__y:
      al.append(('y',self.__y))
    if self.__xunits:
      al.append(('xunits',self.__xunits))
    if self.__yunits:
      al.append(('yunits',self.__yunits))
    return al


class overlayXY(vec2Type):

  def __init__(self):
    vec2Type.__init__(self)

  def xml(self):
    al = self.attributes()
    return ComplexElement('overlayXY', al, None, None, None)


class screenXY(vec2Type):

  def __init__(self):
    vec2Type.__init__(self)

  def xml(self):
    al = self.attributes()
    return ComplexElement('screenXY', al, None, None, None)


class rotationXY(vec2Type):

  def __init__(self):
    vec2Type.__init__(self)

  def xml(self):
    al = self.attributes()
    return ComplexElement('rotationXY', al, None, None, None)


class size(vec2Type):

  def __init__(self):
    vec2Type.__init__(self)

  def xml(self):
    al = self.attributes()
    return ComplexElement('size', al, None, None, None)


class ScreenOverlay(Overlay):

  def __init__(self):
    Overlay.__init__(self)
    self.__overlayXY = None
    self.__screenXY = None
    self.__rotationXY = None
    self.__size = None
    self.__rotation = None

  def Set_overlayXY(self, overlayXY):
    self.__overlayXY = overlayXY

  def Set_screenXY(self, screenXY):
    self.__screenXY = screenXY

  def Set_rotationXY(self, rotationXY):
    self.__rotationXY = rotationXY

  def Set_size(self, size):
    self.__size = size

  def Set_rotation(self, rotation):
    self.__rotation = rotation

  overlayXY = property(fset=Set_overlayXY)
  screenXY = property(fset=Set_screenXY)
  rotationXY = property(fset=Set_rotationXY)
  size = property(fset=Set_size)
  rotation = property(fset=Set_rotation)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = Overlay.children(self)
    if self.__overlayXY:
      children.append(self.__overlayXY)
    if self.__screenXY:
      children.append(self.__screenXY)
    if self.__rotationXY:
      children.append(self.__rotationXY)
    if self.__size:
      children.append(self.__size)
    if self.__rotation:
      children.append(SimpleElement('rotation',self.__rotation))
    return ComplexElement('ScreenOverlay', al, None, el, "".join(children))


class StyleSelector(Object):

  """ """


class Style(StyleSelector):

  """<Style>...</Style>
  """

  def __init__(self):
    StyleSelector.__init__(self)
    self.__iconstyle = None
    self.__labelstyle = None
    self.__linestyle = None
    self.__polystyle = None
    self.__balloonstyle = None
    self.__liststyle = None

  def Set_IconStyle(self, iconstyle):
    self.__iconstyle = iconstyle

  def Set_LabelStyle(self, labelstyle):
    self.__labelstyle = labelstyle

  def Set_LineStyle(self, linestyle):
    self.__linestyle = linestyle

  def Set_PolyStyle(self, polystyle):
    self.__polystyle = polystyle

  def Set_BalloonStyle(self, balloonstyle):
    self.__balloonstyle = balloonstyle

  def Set_ListStyle(self, liststyle):
    self.__liststyle = liststyle

  IconStyle = property(fset=Set_IconStyle)
  LabelStyle = property(fset=Set_LabelStyle)
  LineStyle = property(fset=Set_LineStyle)
  PolyStyle = property(fset=Set_PolyStyle)
  BalloonStyle = property(fset=Set_BalloonStyle)
  ListStyle = property(fset=Set_ListStyle)

  def children(self):
    children = []
    if self.__iconstyle:
      children.append(self.__iconstyle)
    if self.__labelstyle:
      children.append(self.__labelstyle)
    if self.__linestyle:
      children.append(self.__linestyle)
    if self.__polystyle:
      children.append(self.__polystyle)
    if self.__balloonstyle:
      children.append(self.__balloonstyle)
    if self.__liststyle:
      children.append(self.__liststyle)
    return "".join(children)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = self.children()
    return ComplexElement('Style', al, None, el, children)


class ColorStyle(Object):

  def __init__(self):
    Object.__init__(self)
    self.__color = None
    self.__colorMode = None

  def Set_color(self, color):
    self.__color = color

  def Set_colorMode(self, colormode):
    self.__colormode = colormode

  color = property(fset=Set_color)
  colorMode = property(fset=Set_colorMode)

  def elements(self):
    el = Object.elements(self)
    if self.__color:
      el.append(('color',self.__color))
    if self.__colorMode:
      el.append(('colorMode',self.__colorMode))
    return el


class hotSpot(vec2Type):

  """<hotSpot>...</hotSpot>"""

  def __init__(self):
    vec2Type.__init__(self)

  def xml(self):
    al = self.attributes()
    return ComplexElement('hotSpot', al, None, None, None)


class IconStyle(ColorStyle):

  """<IconStyle>...</IconStyle>"""

  def __init__(self):
    ColorStyle.__init__(self)
    self.__scale = None
    self.__icon = None
    self.__hotSpot = None

  def Set_scale(self, scale):
    self.__scale = scale

  def Set_Icon(self, icon):
    self.__icon = icon

  def Set_hotSpot(self, hotSpot):
    self.__hotSpot = hotSpot

  scale = property(fset=Set_scale)
  Icon = property(fset=Set_Icon)
  hotSpot = property(fset=Set_hotSpot)

  def elements(self):
    el = ColorStyle.elements(self)
    if self.__scale:
      el.append(('scale',self.__scale))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = []
    if self.__icon:
      children.append(self.__icon)
    if self.__hotSpot:
      children.append(self.__hotSpot)
    return ComplexElement('IconStyle', al, None, el, "".join(children))


class LineStyle(ColorStyle):

  """<LineStyle>...</LineStyle>"""

  def __init__(self):
    ColorStyle.__init__(self)
    self.__width = None

  def Set_width(self, width):
    self.__width = width

  width = property(fset=Set_width)

  def elements(self):
    el = ColorStyle.elements(self)
    if self.__width:
      el.append(('width',self.__width))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('LineStyle', al, None, el, None)


class PolyStyle(ColorStyle):

  """<PolyStyle>...</PolyStyle>"""

  def __init__(self):
    ColorStyle.__init__(self)
    self.__fill = None
    self.__outline = None

  def Set_fill(self, fill):
    self.__fill = fill

  def Set_outline(self, outline):
    self.__outline = outline

  fill = property(fset=Set_fill)
  outline = property(fset=Set_outline)

  def elements(self):
    el = ColorStyle.elements(self)
    if self.__fill:
      el.append(('fill',self.__fill))
    if self.__outline:
      el.append(('outline',self.__outline))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('PolyStyle', al, None, el, None)


class LabelStyle(ColorStyle):

  """<LabelStyle>...</LabelStyle>"""

  def __init__(self):
    ColorStyle.__init__(self)
    self.__scale = None

  def Set_scale(self, scale):
    self.__scale = scale

  scale = property(fset=Set_scale)

  def elements(self):
    el = ColorStyle.elements(self)
    if self.__scale:
      el.append(('scale',self.__scale))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('LabelStyle', al, None, el, None)


class ListStyle(Object):

  """<ListStyle>...</ListStyle>"""

  def __init__(self):
    Object.__init__(self)
    self.__bgColor = None
    self.__listitemtype = None

  def Set_bgColor(self, bgColor):
    self.__bgColor = bgColor

  def Set_listItemType(self, listitemtype):
    self.__listitemtype = listitemtype

  bgColor = property(fset=Set_bgColor)
  listItemType = property(fset=Set_listItemType)

  def elements(self):
    el = Object.elements(self)
    if self.__bgColor:
      el.append(('bgColor',self.__bgColor))
    if self.__listitemtype:
      el.append(('listItemType',self.__listitemtype))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('ListStyle', al, None, el, None)


class BalloonStyle(Object): 

  def __init__(self):
    Object.__init__(self)
    self.__bgColor = None
    self.__textColor = None
    self.__text = None

  def Set_bgColor(self, bgcolor):
    self.__bgColor = bgcolor

  def Set_textColor(self, textColor):
    self.__textColor = textColor

  def Set_text(self, text):
    self.__text = text

  bgColor = property(fset=Set_bgColor)
  textColor = property(fset=Set_textColor)
  text = property(fset=Set_text)

  def elements(self):
    el = Object.elements(self)
    if self.__bgColor:
      el.append(('bgColor',self.__bgColor))
    if self.__textColor:
      el.append(('textColor',self.__textColor))
    if self.__text:
      el.append(('text',self.__text))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('BalloonStyle', al, None, el, None)


class Pair(object):
  def __init__(self):
    self.__key = None
    self.__styleUrl = None

  def Set_key(self, key):
    self.__key = key

  def Set_styleUrl(self, styleurl):
    self.__styleUrl = styleurl

  key = property(fset=Set_key)
  styleUrl = property(fset=Set_styleUrl)

  def elements(self):
    el = []
    if self.__key:
      el.append(('key',self.__key))
    if self.__styleUrl:
      el.append(('styleUrl',self.__styleUrl))
    return el

  def xml(self):
    el = self.elements()
    return ComplexElement('Pair', None, None, el, None)


class StyleMap(StyleSelector):

  """<StyleMap>...</StyleMap>"""

  def __init__(self):
    StyleSelector.__init__(self)
    self.__pair = []

  def Add_Pair(self, pair):
    self.__pair.append(pair)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = []
    for pair in self.__pair:
      children.append(pair)
    return ComplexElement('StyleMap', al, None, el, "".join(children))


class TimeSpan(Object):

  def __init__(self):
    Object.__init__(self)
    self.__begin = None
    self.__end = None

  def Set_begin(self, begin):
    self.__begin = begin

  def Get_begin(self):
    return self.__begin

  def Set_end(self, end):
    self.__end = end

  def Get_end(self):
    return self.__end

  begin = property(fset=Set_begin,fget=Get_begin)
  end = property(fset=Set_end,fget=Get_end)

  def elements(self):
    el = []
    if self.__begin:
      el.append(('begin',self.__begin))
    if self.__end:
      el.append(('end',self.__end))
    return el

  def xml(self):
    at = self.attributes()
    el = self.elements()
    return ComplexElement('TimeSpan', at, None, el, None)


class TimeStamp(Object):

  def __init__(self):
    Object.__init__(self)
    self.__when = None

  def Set_when(self, when):
    self.__when = when

  when = property(fset=Set_when)

  def elements(self):
    el = []
    if self.__when:
      el.append(('when',self.__when))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('TimeStamp', al, None, el, None)


class Update(object):

  def __init__(self):
    self.__targetHref = None
    self.__operations = []

  def Set_targetHref(self, targetHref):
    self.__targetHref = targetHref

  def Add_Operation(self, operation):
    self.__operations.append(operation)

  targetHref = property(fset=Set_targetHref)

  def elements(self):
    el = []
    if self.__targetHref:
      el.append(('targetHref',self.__targetHref))
    return el

  def xml(self):
    el = self.elements()
    return ComplexElement('Update', None, None, el, "".join(self.__operations))


class Delete(object):

  def __init__(self):
    self.__objects = []

  def Add_Object(self,object):
    self.__objects.append(object)

  def xml(self):
    return ComplexElement('Delete', None, None, None, "".join(self.__objects))


class Change(object):

  def __init__(self):
    self.__objects = []

  def Add_Object(self,object):
    self.__objects.append(object)

  def xml(self):
    return ComplexElement('Change', None, None, None, "".join(self.__objects))


class Create(object):

  def __init__(self):
    self.__objects = []
    self.__folder = None

  def Set_folder(self, folder):
    self.__folder = folder

  Folder = property(fset=Set_folder)

  def xml(self):
    return ComplexElement('Create', None, None, None, self.__folder)


class Location(Object):

  """<Location>...</Location>
  """

  def __init__(self):
    Object.__init__(self)
    self.__latitude = None
    self.__longitude = None
    self.__altitude = None

  def Set_latitude(self, latitude):
    self.__latitude = latitude

  def Get_latitude(self):
    return self.__latitude

  def Set_longitude(self, longitude):
    self.__longitude = longitude

  def Get_longitude(self):
    return self.__longitude

  def Set_altitude(self, altitude):
    self.__altitude = altitude

  def Get_altitude(self):
    return self.__altitude

  latitude = property(fset=Set_latitude, fget=Get_latitude)
  longitude = property(fset=Set_longitude, fget=Get_longitude)
  altitude = property(fset=Set_altitude, fget=Get_altitude)

  def elements(self):
    el = []
    if self.__latitude:
      el.append(('latitude',self.__latitude))
    if self.__longitude:
      el.append(('longitude',self.__longitude))
    if self.__altitude:
      el.append(('altitude',self.__altitude))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('Location', al, None, el, None)

      
class Orientation(Object):
  """     
  """     
  def __init__(self):
    Object.__init__(self)
    self.__heading = None
    self.__tilt = None
    self.__roll = None

  def Set_heading(self, heading):
    self.__heading = heading

  def Get_heading(self):
    return self.__heading

  def Set_tilt(self, tilt):
    self.__tilt = tilt

  def Get_tilt(self):
    return self.__tilt

  def Set_roll(self, roll):
    self.__roll = roll

  def Get_roll(self):
    return self.__roll

  heading = property(fset=Set_heading, fget=Get_heading)
  tilt = property(fset=Set_tilt, fget=Get_tilt)
  roll = property(fset=Set_roll, fget=Get_roll)

  def elements(self):
    el = []
    if self.__heading:
      el.append(('heading',self.__heading))
    if self.__tilt:
      el.append(('tilt',self.__tilt))
    if self.__roll:
      el.append(('roll',self.__roll))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('Orientation', al, None, el, None)
          
class Scale(Object):
  """     
  """  
  def __init__(self):
    Object.__init__(self)
    self.__x = None
    self.__y = None
    self.__z = None

  def Set_x(self, x):
    self.__x = x

  def Get_x(self):
    return self.__x

  def Set_y(self, y):
    self.__y = y

  def Get_y(self):
    return self.__y

  def Set_z(self, z):
    self.__z = z

  def Get_z(self):
    return self.__z

  x = property(fset=Set_x, fget=Get_x)
  y = property(fset=Set_y, fget=Get_y)
  z = property(fset=Set_z, fget=Get_z)

  def elements(self):
    el = []
    if self.__x:
      el.append(('x',self.__x))
    if self.__y:
      el.append(('y',self.__y))
    if self.__z:
      el.append(('z',self.__z))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('Scale', al, None, el, None)
     

class Alias(Object):
  """<Alias>...</Alias>
  """
  def __init__(self):
    Object.__init__(self)
    self.__targetHref = None
    self.__sourceHref = None

  def Set_targetHref(self, targetHref):
    self.__targetHref = targetHref

  def Get_targetHref(self):
    return self.__targetHref

  def Set_sourceHref(self, sourceHref):
    self.__sourceHref = sourceHref

  def Get_sourceHref(self):
    return self.__sourceHref

  targetHref = property(fset=Set_targetHref, fget=Get_targetHref)
  sourceHref = property(fset=Set_sourceHref, fget=Get_sourceHref)

  def elements(self):
    el = []
    if self.__targetHref:
      el.append(('targetHref',self.__targetHref))
    if self.__sourceHref:
      el.append(('sourceHref',self.__sourceHref))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('Alias', al, None, el, None)


class ResourceMap(Object):

  """<ResourceMap>...</ResourceMap>
  """

  def __init__(self):
    Object.__init__(self)
    self.__AliasList = []

  def Add_Alias(self, alias):
    self.__AliasList.append(alias)

  def xml(self):
    children = []
    for alias in self.__AliasList:
      children.append(alias)
    return ComplexElement('ResourceMap', None, None, None, "".join(children))


class Model(Object):

  """<Model>...</Model>
  """

  def __init__(self):
    Object.__init__(self)
    self.__Location = None
    self.__Orientation = None
    self.__Scale = None
    self.__Link = None
    self.__ResourceMap = None

  def Set_Location(self, Location):
    self.__Location = Location

  def Set_Orientation(self, Orientation):
    self.__Orientation = Orientation

  def Set_Scale(self, Scale):
    self.__Scale = Scale

  def Set_Link(self, Link):
    self.__Link = Link

  def Set_ResourceMap(self, ResourceMap):
    self.__ResourceMap = ResourceMap

  Location = property(fset=Set_Location)
  Orientation = property(fset=Set_Orientation)
  Scale = property(fset=Set_Scale)
  Link = property(fset=Set_Link)
  ResourceMap = property(fset=Set_ResourceMap)

  def xml(self):
    al = self.attributes()
    children = []
    if self.__Location:
      children.append(self.__Location)
    if self.__Orientation:
      children.append(self.__Orientation)
    if self.__Scale:
      children.append(self.__Scale)
    if self.__Link:
      children.append(self.__Link)
    if self.__ResourceMap:
      children.append(self.__ResourceMap)

    return ComplexElement('Model', al, None, None, "".join(children))


class ViewVolume(Object):

  """<ViewVolume>...</ViewVolume>
  """

  def __init__(self):
    Object.__init__(self)
    self.__leftFov = None
    self.__rightFov = None
    self.__bottomFov = None
    self.__topFov = None
    self.__near = None

  def Set_leftFov(self, leftFov):
    self.__leftFov = leftFov

  def Get_leftFov(self):
    return self.__leftFov

  def Set_rightFov(self, rightFov):
    self.__rightFov = rightFov

  def Get_rightFov(self):
    return self.__rightFov

  def Set_bottomFov(self, bottomFov):
    self.__bottomFov = bottomFov

  def Get_bottomFov(self):
    return self.__bottomFov

  def Set_topFov(self, topFov):
    self.__topFov = topFov

  def Get_topFov(self):
    return self.__topFov

  def Set_near(self, near):
    self.__near = near

  def Get_near(self):
    return self.__near

  leftFov = property(fset=Set_leftFov, fget=Get_leftFov)
  rightFov = property(fset=Set_rightFov, fget=Get_rightFov)
  bottomFov = property(fset=Set_bottomFov, fget=Get_bottomFov)
  topFov = property(fset=Set_topFov, fget=Get_topFov)
  near = property(fset=Set_near, fget=Get_near)

  def elements(self):
    el = []
    if self.__leftFov:
      el.append(('leftFov',self.__leftFov))
    if self.__rightFov:
      el.append(('rightFov',self.__rightFov))
    if self.__bottomFov:
      el.append(('bottomFov',self.__bottomFov))
    if self.__topFov:
      el.append(('topFov',self.__topFov))
    if self.__near:
      el.append(('near',self.__near))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('ViewVolume', al, None, el, None)


class ImagePyramid(Object):

  """<ImagePyramid>...</ImagePyramid>
  """

  def __init__(self):
    Object.__init__(self)
    self.__tileSize = None
    self.__maxWidth = None
    self.__maxHeight = None

  def Set_tileSize(self, tileSize):
    self.__tileSize = tileSize

  def Get_tileSize(self):
    return self.__tileSize

  def Set_maxWidth(self, maxWidth):
    self.__maxWidth = maxWidth

  def Get_maxWidth(self):
    return self.__maxWidth

  def Set_maxHeight(self, maxHeight):
    self.__maxHeight = maxHeight

  def Get_maxHeight(self):
    return self.__maxHeight

  tileSize = property(fset=Set_tileSize, fget=Get_tileSize)
  maxWidth = property(fset=Set_maxWidth, fget=Get_maxWidth)
  maxHeight = property(fset=Set_maxHeight, fget=Get_maxHeight)

  def elements(self):
    el = []
    if self.__tileSize:
      el.append(('tileSize',self.__tileSize))
    if self.__maxWidth:
      el.append(('maxWidth',self.__maxWidth))
    if self.__maxHeight:
      el.append(('maxHeight',self.__maxHeight))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('ImagePyramid', al, None, el, None)


class PhotoOverlay(Overlay):

  """<PhotoOverlay>...</PhotoOverlay>
  """

  def __init__(self):
    Overlay.__init__(self)
    self.__shape = None
    self.__ViewVolume = None
    self.__roll = None
    self.__ImagePyramid = None
    self.__Point = None

  def Set_shape(self, shape):
    self.__shape = shape

  def Set_ViewVolume(self, ViewVolume):
    self.__ViewVolume = ViewVolume

  def Set_roll(self, roll):
    self.__roll = roll

  def Set_ImagePyramid(self, ImagePyramid):
    self.__ImagePyramid = ImagePyramid

  def Set_Point(self, Point):
    self.__Point = Point

  shape = property(fset=Set_shape)
  ViewVolume = property(fset=Set_ViewVolume)
  roll = property(fset=Set_roll)
  ImagePyramid = property(fset=Set_ImagePyramid)
  Point = property(fset=Set_Point)

  def xml(self):
    al = self.attributes()
    el = self.elements()
    children = Overlay.children(self)
    if self.__shape:
      children.append(SimpleElement('shape',self.__shape))
    if self.__ViewVolume:
      children.append(self.__ViewVolume)
    if self.__roll:
      children.append(SimpleElement('roll',self.__roll))
    if self.__ImagePyramid:
      children.append(self.__ImagePyramid)
    if self.__Point:
      children.append(self.__Point)

    return ComplexElement('PhotoOverlay', al, None, el, "".join(children))
