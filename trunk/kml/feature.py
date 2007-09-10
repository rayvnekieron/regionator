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

def PrintFeatureToString(name, depth):
  str = []
  d = 0
  while d < depth:
    str.append(' ')
    d += 1
  str.append(name)
  str.append('\n')
  return ''.join(str)
    
def PrintFeaturesToString(doc, feature_list, depth):
  """Print the Feature hierarchy to string

  Recurses on each Container Feature in the list.

  Args:
    doc: xml.dom.minidom DOCUMENT_NODE
    feature_list: list of xml.dom.minidom ELEMENT_NODE children of doc
    depth: current hierarchy (indent) depth

  Returns:
    string: hierarchy of Feature names indented Pythonically by depth
  """
  lines = []
  for feature in feature_list:
    lines.append(PrintFeatureToString(feature.tagName, depth))
    if IsContainer(feature):
      lines.append(PrintFeaturesToString(doc, FindFeaturesInDoc(feature), depth+1))
  return ''.join(lines)

def PrintFeaturesInFile(url):
  """Print the Feature hierarchy to stdout

  Args:
    url: KML/KMZ file/url
  """
  (doc, feature_list) = FindFeaturesInFile(url)
  print PrintFeaturesToString(doc, feature_list, 0),
  
    
