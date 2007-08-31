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

import math
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

def ParsePhotoOverlay(po_node):
  icon_node = None
  vvol_node = None
  pyr_node = None
  point_node = None
  for child in po_node.childNodes:
    if child.nodeType != child.ELEMENT_NODE:
      continue
    if child.tagName == 'Icon':
      icon_node = child
    elif child.tagName == 'ViewVolume':
      vvol_node = child
    elif child.tagName == 'ImagePyramid':
      pyr_node = child
    elif child.tagName == 'Point':
      point_node = child
  return (icon_node, vvol_node, pyr_node, point_node)

def ParseImagePyramid(pyr_node):
  tile_size = kml.kmlparse.GetSimpleElementText(pyr_node, 'tileSize')
  if not tile_size:
    tile_size = 256
  max_width = kml.kmlparse.GetSimpleElementText(pyr_node, 'maxWidth')
  max_height = kml.kmlparse.GetSimpleElementText(pyr_node, 'maxHeight')
  grid_origin = kml.kmlparse.GetSimpleElementText(pyr_node, 'gridOrigin')
  return (int(tile_size), int(max_width), int(max_height), grid_origin)

def CheckPhotoOverlayElements(icon_node, vvol_node, pyr_node, point_node):
  # A realistic PhotoOverlay must have these 4 children
  if not icon_node or not vvol_node or not pyr_node or not point_node:
    return False
  # The Icon must have an href
  href = kml.kmlparse.GetSimpleElementText(icon_node, 'href')
  if not ValidHref(href):
    return False
  (tile_size, max_width, max_height, grid_origin) = ParseImagePyramid(pyr_node)
  if tile_size & (tile_size-1):
    return False
  return True

def MaxLevelRowCol(tile_size, max_wid, max_ht):
  """
  w == h == 256 -> (0, 0, 0)
  w == h == 512 -> (1, 1, 1)
  w == h == 1024 -> (2, 2, 2)
  Args:
    max_wid, max_ht: maxWidth,maxHeight
    tile_size: w/h of a tile in pixels (must be ^2 and square)
  Returns:
    (max_level, max_row, max_col): maximum for each
  """
  width_in_tiles = int(math.ceil(float(max_wid)/float(tile_size)))
  height_in_tiles = int(math.ceil(float(max_ht)/float(tile_size)))
  lh = math.ceil(math.log(width_in_tiles, 2))
  lw = math.ceil(math.log(height_in_tiles, 2))
  level = int(max(lh, lw))
  return (level, height_in_tiles-1, width_in_tiles-1)

def GetPhotoOverlayHrefs(href, tile_size, max_wid, max_ht):
  (max_level, max_row, max_col) = MaxLevelRowCol(tile_size, max_wid, max_ht)
  href_list = []
  # Find the deepest corners
  if max_level > 0:
    href_list.append(ExpandImagePyramidHref(href, max_level, max_col, max_row))
    href_list.append(ExpandImagePyramidHref(href, max_level, 0, max_row))
    href_list.append(ExpandImagePyramidHref(href, max_level, max_col, 0))
    href_list.append(ExpandImagePyramidHref(href, max_level, 0, 0))
  # There's always this tile
  href_list.append(ExpandImagePyramidHref(href, 0, 0, 0))
  return href_list

def CheckPhotoOverlay(parent_href, po_node, verbose):
  if po_node.nodeType != po_node.ELEMENT_NODE:
    return False
  if po_node.tagName != 'PhotoOverlay':
    return False
  (icon_node, vvol_node, pyr_node, point_node) = ParsePhotoOverlay(po_node)
  if not CheckPhotoOverlayElements(icon_node, vvol_node, pyr_node, point_node):
    return False
  (tile_size, max_wid, max_ht, grid_origin) = ParseImagePyramid(pyr_node)
  href = kml.kmlparse.GetSimpleElementText(icon_node, 'href')
  href_list = GetPhotoOverlayHrefs(href, tile_size, max_wid, max_ht)
  error_count = 0
  for href in href_list:
    href = kml.href.ComputeChildUrl(parent_href, href)
    fetcher = kml.href.Fetcher(href)
    data = fetcher.FetchData()
    if verbose:
      print href, len(data)
      if not data:
        print 'Failed to fetch',href
        error_count += 1
  return error_count == 0

def CheckPhotos(url, verbose):
  kp = kml.kmlparse.KMLParse(url)
  if not kp.Doc():
    return
  for po_node in kp.Doc().getElementsByTagName('PhotoOverlay'):
    name = kml.kmlparse.GetSimpleElementText(po_node, 'name')
    if verbose:
      print 'checking',name
    CheckPhotoOverlay(url, po_node, verbose)

