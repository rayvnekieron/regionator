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
  styleUrl = property(fset=Set_styleUrl)
  TimePrimitive = property(fset=Set_TimePrimitive)
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
    return ComplexElement('Document', al, None, el, "".join(children))


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
    al = Feature.attributes(self)
    el = Feature.elements(self)
    return ComplexElement('NetworkLink', al, None, el, self.__Link)


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
    el = []
    if self.__href:
      el.append(('href',self.__href))
    if self.__viewRefreshMode:
      el.append(('viewRefreshMode',self.__viewRefreshMode))
    if self.__viewRefreshTime:
      el.append(('viewRefreshTime',self.__viewRefreshTime))
    return el

  def xml(self):
    el = self.elements()
    return ComplexElement('Link', None, None, el, None)


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


