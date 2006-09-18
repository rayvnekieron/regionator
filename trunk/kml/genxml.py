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

  # XXX handle empty tag (<foo/>)

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
    return ComplexElement('kml', al, comment, None, "".join(children))


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
    if self.__styleUrl: # XXX simple type
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
    return ComplexElement('Document', None, al, el, "".join(children))

