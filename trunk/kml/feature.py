"""
Copyright (C) 2007 Google Inc.

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

import xml.dom.minidom
import kml.kmlparse

def IsFeature(node):
  return node.tagName == 'Placemark' or node.tagName == 'NetworkLink' or \
         IsContainer(node) or IsOverlay(node)

def IsContainer(node):
  return node.tagName == 'Folder' or node.tagName == 'Document'

def IsOverlay(node):
  return node.tagName == 'GroundOverlay' or \
         node.tagName == 'ScreenOverlay' or \
         node.tagName == 'PhotoOverlay'

def GetChildFeatures(node):
  return GetFeatureElementsInDoc(node)

def GetFeatureElementsInDoc(doc):
  feature_list = []
  for child in doc.childNodes:
    if child.nodeType != child.ELEMENT_NODE:
      continue
    if IsFeature(child):
     feature_list.append(child)
  return feature_list

def FindFeaturesInDoc(doc):
  """
  Args:
    doc: an xml.dom.minidom DOCUMENT_NODE
  Return:
    features: a list of Feature ELEMENT_NODEs in the doc
  """
  # A .kml file has one Feature.  The Feature is either the root element,
  # or the child of the <kml> root element.
  k = kml.kmlparse.GetFirstChildElement(doc, 'kml')
  if k:
    doc = k
  return GetFeatureElementsInDoc(doc)

def FindFeaturesInFile(url):
  kp = kml.kmlparse.KMLParse(url)
  doc = kp.Doc()
  if not doc:
    return False
  return (doc, FindFeaturesInDoc(doc))

def Indent(name, indent_spaces):
  str = []
  i = 0
  while i < indent_spaces:
    str.append(' ')
    i += 1
  str.append(name)
  return ''.join(str)
    
class FeatureNodeHandler:
  def HandleFeatureNode(self, kml_url, depth, feature_node):
    """Called on each node in the Feature hierarchy

    Abstract base class.  Extended this and define HandleFeatureNode.
    Use your derived class with FeatureHierarchy.SetNodeHandler().

    Args:
      url: URL to the kmlfile of this feature
      feature_node: xml.dom.minidom ELEMENT_NODE
    """

class FeatureHierarchy:
  """Walk the Feature hierarchy of a KML file"""
  def __init__(self):
    self.__node_handler = None
    self.__doc = None
    self.__root_feature_node = None
    self.__kml_url = None

  def SetNodeHandler(self, node_handler):
    self.__node_handler = node_handler

  def WalkString(self, kml):
    doc = xml.dom.minidom.parseString(kml)
    feature_list = FindFeaturesInDoc(xml.dom.minidom.parseString(kml))
    return self._Walk(doc, feature_list)

  def WalkFile(self, kml_url):
    (doc, feature_list) = FindFeaturesInFile(kml_url)
    self.__kml_url = kml_url
    return self._Walk(doc, feature_list)

  def _Walk(self, doc, feature_list):
    if len(feature_list) > 1:
      # Invalid KML file
      return False
    self.__doc = doc
    self.__root_feature_node = feature_list[0]
    return self._VisitFeatureNode(self.__root_feature_node, 0)

  def _VisitFeatureNode(self, feature_node, depth):
    if self.__node_handler:
      self.__node_handler.HandleFeatureNode(self.__kml_url, depth,
                                            feature_node)
      
    if IsContainer(feature_node):
      feature_node_list = GetChildFeatures(feature_node)
      for feature_node in feature_node_list:
        self._VisitFeatureNode(feature_node, depth+1)


class FeaturePrinter(FeatureNodeHandler):
  def __init__(self, print_name, print_id):
    self.__print_name = print_name
    self.__print_id = print_id
    self.__output_lines = []

  def GetOutput(self):
    return '\n'.join(self.__output_lines)

  def HandleFeatureNode(self, kml_url, depth, feature_node):
    this_line = []
    this_line.append(Indent(feature_node.tagName, depth))
    # XXX id
    if self.__print_name:
      name = kml.kmlparse.GetSimpleElementText(feature_node, 'name')
      if name:
        this_line.append('[%s]' % name)
    self.__output_lines.append(' '.join(this_line))


class FeatureCounter(FeatureNodeHandler):
  def __init__(self):
    self.__feature_count_map = {}
    self.__max_depth = 0

  def GetFeatureCountMap(self):
    return self.__feature_count_map

  def _IncrementCount(self, feature_name):
    if self.__feature_count_map.has_key(feature_name):
      self.__feature_count_map[feature_name] += 1
    else:
      self.__feature_count_map[feature_name] = 1

  def HandleFeatureNode(self, kml_url, depth, feature_node):
    self._IncrementCount(feature_node.tagName)

def CountFeatures(kml_url):
  print kml_url
  feature_counter = FeatureCounter()
  feature_hierarchy = FeatureHierarchy()
  feature_hierarchy.SetNodeHandler(feature_counter)
  feature_hierarchy.WalkFile(kml_url)
  feature_count_map = feature_counter.GetFeatureCountMap()
  for feature_name in feature_count_map.keys():
    print feature_name,feature_count_map[feature_name]

def PrintFeaturesInString(kml):
  feature_printer = FeaturePrinter(True, True)
  feature_hierarchy = FeatureHierarchy()
  feature_hierarchy.SetNodeHandler(feature_printer)
  feature_hierarchy.WalkString(kml)
  return feature_printer.GetOutput()

def PrintFeaturesInFile(url, verbose):
  """Print the Feature hierarchy to stdout

  Args:
    url: KML/KMZ file/url
  """
  feature_printer = FeaturePrinter(True, True)
  feature_hierarchy = FeatureHierarchy()
  feature_hierarchy.SetNodeHandler(feature_printer)
  feature_hierarchy.WalkFile(url)
  if verbose:
    print feature_printer.GetOutput()

