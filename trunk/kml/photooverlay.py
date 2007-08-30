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

import kml.href
import kml.kmlparse

def ValidHref(href):
  """ A PhotoOverlay href has $[level] and $[x] and $[y] """
  if not href:
    return False
  level_index = href.find('$[level]')
  x_index = href.find('$[x]')
  y_index = href.find('$[y]')
  # Must have all three
  if level_index == -1 or x_index == -1 or y_index == -1:
    return False
  # Expand level,x,y and ensure the result is valid
  # This will catch a duplicate $[blah]
  dummy = ExpandImagePyramidHref(href, 0, 0, 0)
  return kml.href.AreAllCharsGood(dummy)

def ExpandImagePyramidHref(href, level, x, y):
  """ Replace $[level], $[x], and $[y]
  Args:
    level,x,y: int
  Returns:
    href: $[level],$[x],$[y], replaced with args
  """
  level = repr(level)
  x = repr(x)
  y = repr(y)
  return href.replace('$[level]', level).replace('$[x]', x).replace('$[y]', y)

def ValidWidHt(a):
  """ a > 0 and ^2 """
  return (a > 0) and not (a & (a-1))

def ParsePhotoOverlay(po_node):
  icon_node = None
  vvol_node = None
  impyr_node = None
  point_node = None
  for child in po_node.childNodes:
    if child.nodeType != child.ELEMENT_NODE:
      continue
    if child.tagName == 'Icon':
      icon_node = child
    elif child.tagName == 'ViewVolume':
      vvol_node = child
    elif child.tagName == 'ImagePyramid':
      impyr_node = child
    elif child.tagName == 'Point':
      point_node = child
  return (icon_node, vvol_node, impyr_node, point_node)

def CheckPhotoOverlayNode(po_node):
  if po_node.nodeType != po_node.ELEMENT_NODE:
    return False
  if po_node.tagName != 'PhotoOverlay':
    return False
  (icon_node, vvol_node, impyr_node, point_node) = ParsePhotoOverlay(po_node)
  # A realistic PhotoOverlay must have these 4 children
  if not icon_node or not vvol_node or not impyr_node or not point_node:
    return False
  # The Icon must have an href
  href = kml.kmlparse.GetSimpleElementText(icon_node, 'href')
  if not ValidHref(href):
    return False
  max_width = kml.kmlparse.GetSimpleElementText(impyr_node, 'maxWidth')
  max_height = kml.kmlparse.GetSimpleElementText(impyr_node, 'maxHeight')
  if not ValidWidHt(int(max_width)) or not ValidWidHt(int(max_height)):
    return False
  return True

