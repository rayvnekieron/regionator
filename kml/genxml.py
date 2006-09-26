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
    self.__LookAt = None
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

  def Set_LookAt(self, l):
    self.__LookAt = l

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
  LookAt = property(fset=Set_LookAt)
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
    return el

  def children(self):
    children = []
    if self.__LookAt:
      children.append(self.__LookAt)
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

  def Set_href(self, href):
    self.__href = href

  def Set_viewRefreshMode(self, viewRefreshMode):
    self.__viewRefreshMode = viewRefreshMode

  def Set_viewRefreshTime(self, viewRefreshTime):
    self.__viewRefreshTime = viewRefreshTime

  href = property(fset=Set_href)
  viewRefreshMode = property(fset=Set_viewRefreshMode)
  viewRefreshTime = property(fset=Set_viewRefreshTime)

  def elements(self):
    el = Object.elements(self)
    if self.__href:
      el.append(('href',self.__href))
    if self.__viewRefreshMode:
      el.append(('viewRefreshMode',self.__viewRefreshMode))
    if self.__viewRefreshTime:
      el.append(('viewRefreshTime',self.__viewRefreshTime))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('Link', al, None, el, None)


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

  def Set_north(self, north):
    """ string """
    self.__north = north

  def Set_south(self, south):
    """ string """
    self.__south = south

  def Set_east(self, east):
    """ string """
    self.__east = east

  def Set_west(self, west):
    """ string """
    self.__west = west

  north = property(fset=Set_north)
  south = property(fset=Set_south)
  east = property(fset=Set_east)
  west = property(fset=Set_west)

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
    self.__minaltitude = None
    self.__maxaltitude = None
    self.__altitudemode = None

  def Set_minAltitude(self, minaltitude):
    self.__minaltitude = minaltitude

  def Set_maxAltitude(self, maxaltitude):
    self.__maxaltitude = maxaltitude

  def Set_altitudeMode(self, altitudemode):
    self.__altitudemode = altitudemode

  minAltitude = property(fset=Set_minAltitude)
  maxAltitude = property(fset=Set_maxAltitude)
  altitudeMode = property(fset=Set_altitudeMode)

  def elements(self):
    el = LatLonBox.elements(self)
    if self.__minaltitude:
      el.append(('minAltitude',self.__minaltitude))
    if self.__maxaltitude:
      el.append(('maxAltitude',self.__maxaltitude))
    if self.__altitudemode:
      el.append(('altitudeMode',self.__altitudemode))
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

  def Set_maxLodPixels(self, maxlodpixels):
    self.__maxlodpixels = maxlodpixels

  def Set_minFadeExtent(self, minfadeextent):
    self.__minfadeextent = minfadeextent

  def Set_maxFadeExtent(self, maxfadeextent):
    self.__maxfadeextent = maxfadeextent

  minLodPixels = property(fset=Set_minLodPixels)
  maxLodPixels = property(fset=Set_maxLodPixels)
  minFadeExtent = property(fset=Set_minFadeExtent)
  maxFadeExtent = property(fset=Set_maxFadeExtent)

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


class LookAt(Object):

  """<LookAt>...</LookAt>
  """

  def __init__(self):
    Object.__init__(self)
    self.__longitude = None
    self.__latitude = None
    self.__altitude = None
    self.__range = None
    self.__tilt = None
    self.__heading = None
    self.__altitudeMode = None

  def Set_longitude(self, longitude):
    self.__longitude = longitude

  def Set_latitude(self, latitude):
    self.__latitude = latitude

  def Set_altitude(self, altitude):
    self.__altitude = altitude

  def Set_range(self, range):
    self.__range = range

  def Set_tilt(self, tilt):
    self.__tilt = tilt

  def Set_heading(self, heading):
    self.__heading = heading

  def Set_altitudeMode(self, altitudeMode):
    self.__altitudeMode = altitudeMode

  longitude = property(fset=Set_longitude)
  latitude = property(fset=Set_latitude)
  altitude = property(fset=Set_altitude)
  range = property(fset=Set_range)
  tilt = property(fset=Set_tilt)
  heading = property(fset=Set_heading)
  altitudeMode = property(fset=Set_altitudeMode)

  def elements(self):
    el = Object.elements(self)
    if self.__longitude:
      el.append(('longitude',self.__longitude))
    if self.__latitude:
      el.append(('latitude',self.__latitude))
    if self.__altitude:
      el.append(('altitude',self.__altitude))
    if self.__range:
      el.append(('range',self.__range))
    if self.__tilt:
      el.append(('tilt',self.__tilt))
    if self.__heading:
      el.append(('heading',self.__heading))
    if self.__altitudeMode:
      el.append(('altitudeMode',self.__altitudeMode))
    return el

  def xml(self):
    al = self.attributes()
    el = self.elements()
    return ComplexElement('LookAt', al, None, el, None)


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

  def Set_Icon(self, Icon):
    self.__Icon = Icon

  color = property(fset=Set_color)
  drawOrder = property(fset=Set_drawOrder)
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

  def __init(self):
    Overlay.__init__(self)
    self.__latlonbox = None

  def Set_LatLonBox(self, latlonbox):
    self.__latlonbox = latlonbox

  LatLonBox = property(fset=Set_LatLonBox)

  def xml(self):
    al = self.attributes()
    el = self.elements()
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
  textr = property(fset=Set_text)

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

  def Set_end(self, end):
    self.__end = end

  begin = property(fset=Set_begin)
  end = property(fset=Set_end)

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


