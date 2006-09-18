#!/usr/bin/python

import kml.genxml

class SomeElement(object):

  """
  <complexType name="SomeElementType">
    <sequence>
      <element name="name" type="string"/>
      <element name="visibility" type="boolean"/>
      <element name="Foo" type="fooml:FooType"/>
      <element name="Goo" type="fooml:GooType"/>
    </sequence>
  </complexType>
  """

  def __init__(self):
    self.__name = None
    self.__visibility = None
    self.__Foo = None
    self.__Goo = None

  def Set_name(self, name):
    self.__name = name
    
  def Set_visibility(self, visibility):
    self.__visibility = visibility

  def Set_Foo(self, foo):
    self.__Foo = foo

  def Set_Goo(self, goo):
    self.__Goo = goo

  name = property(fset=Set_name)
  visibility = property(fset=Set_visibility)
  Foo = property(fset=Set_Foo)
  Goo = property(fset=Set_Goo)

  def attributes(self):
    return []

  def elements(self):
    el = []
    if self.__name:
      el.append(('name',self.__name))
    if self.__visibility:
      el.append(('visibility',self.__visibility))
    return el

  def children(self):
    children = []
    if self.__Foo:
      children.append(self.__Foo)
    if self.__Goo:
      children.append(self.__Goo)
    return "".join(children)

  def xml(self):
    children = self.children()
    al = self.attributes()
    el = self.elements()
    return kml.genxml.ComplexElement('SomeElement', None, al, el, children)


class Goo(object):

  """
  <complexType name="GooType">
    <sequence>
      <element name="color" type="hexBinary"/>
      <element name="width" type="int"/>
    </sequence>
  </complexType>
  """

  def __init__(self):
    self.__color = None
    self.__width = None

  def Set_color(self, color):
    self.__color = color
    
  def Set_width(self, width):
    self.__width = width

  color = property(fset=Set_color)
  width = property(fset=Set_width)

  def elements(self):
    el = []
    if self.__color:
      el.append(('color',self.__color))
    if self.__width:
      el.append(('width',self.__width))
    return el
    
  def xml(self):
    el = self.elements()
    return kml.genxml.ComplexElement('Goo', None, None, el, None)


class Foo(Goo):

  """
  <complexType name="FooType">
    <complexContent>
      <extension base="fooml:GooType">
        <sequence>
          <element name="x" type="float"/>
          <element name="y" type="float"/>
        </sequence>
      </extension>
    </complexContent>  
  </complexType>
  """

  def __init__(self):
    Goo.__init__(self)
    self.__x = None
    self.__y = None


se = SomeElement()
se.name = 'my name'
se.visibility = '1'
f = open('testxml.xml', 'w')
f.write(se.xml())

goo = Goo()
goo.color = 'ffff0000'
goo.width = 4

se2 = SomeElement()
se2.name = 'my other name'
se2.Goo = goo.xml()
f.write(se2.xml())
f.close()
