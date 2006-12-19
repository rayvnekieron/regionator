#!/usr/bin/python

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

"""

Verify sane Regions in a Region NetworkLink hierarchy 

"""


import sys
import kml.kmlparse
import kml.genxml
import kml.href
import os.path


if len(sys.argv) != 2:
  print 'usage: %s input.kml' % sys.argv[0]
  sys.exit(1)

inputkml = sys.argv[1]

region_count = 0
file_count = 0
error_count = 0


def CheckLatLonBox(name, llb):
  global error_count
  status = True
  # These are _not_ the defaults
  # A common error is for 0 to be take as "not set" (or None)
  if llb.north == None:
    print 'north not set'
    error_count += 1
    llb.north = 0
  if llb.south == None:
    print 'south not set'
    error_count += 1
    llb.south = 0
  if llb.east == None:
    print 'east not set'
    error_count += 1
    llb.east = 0
  if llb.west == None:
    print 'east not set'
    error_count += 1
    llb.west = 0
  if float(llb.north) <= float(llb.south):
    print '%s: north not greater than south' % name
    error_count += 1
    status = False
  if float(llb.east) <= float(llb.west):
    print '%s: east not greater than west' % name
    error_count += 1
    status = False
  return status


def CheckLatLonAltBox(llab):
  global error_count
  status = True
  if not CheckLatLonBox('LatLonAltBox', llab):
    status = False
  if llab.minAltitude and llab.maxAltitude:
    if float(llab.minAltitude) < float(llab.maxAltitude):
      error_count += 1
      print 'east not greater than west'
      status = False
  return status


def CheckLatLonBoxContains(parent_llb, child_llb):
  global error_count
  if parent_llb == None:
    return True
  if (float(parent_llb.north) >= float(child_llb.north) and
      float(parent_llb.south) <= float(child_llb.south) and
      float(parent_llb.east) >= float(child_llb.east) and
      float(parent_llb.west) <= float(child_llb.west)):
    return True
  error_count += 1
  return False


def CheckLod(lod):
  global error_count
  status = True
  if lod.minLodPixels < 0:
    print 'Lod bad minLodPixels',lod.minLodPixels
    error_count += 1
    status = False
  if lod.maxLodPixels == None or float(lod.maxLodPixels) == -1:
    return status

  if float(lod.minLodPixels) > float(lod.maxLodPixels):
    print 'Lod: minLodPixels greater than maxLodPixels'
    error_count += 1
    status = False
  return status


def CheckRegion(region_node):
  print 'Region',
  global region_count
  region_count += 1
  status = True
  (llab_node, lod_node) = kml.kmlparse.ParseRegion(region_node)
  llab = kml.kmlparse.ParseLatLonAltBox(llab_node)
  lod = kml.kmlparse.ParseLod(lod_node)
  if not CheckLatLonAltBox(llab):
    status = False
  if not CheckLod(lod):
    status = False
  if status:
    print 'ok'
  return status


def RelativeName(parent_path, relative_path):
  # XXX presumes relative_path is just that...
  dir = os.path.dirname(parent_path)
  return os.path.join(dir, relative_path)


def GetLinkHref(link_node):
  link = kml.kmlparse.ParseLink(link_node)
  return link.href


def GetNetworkLinkFile(networklink_node):
  # XXX or <Url>
  link_nodelist = networklink_node.getElementsByTagName('Link')
  if link_nodelist:
    return GetLinkHref(link_nodelist[0])
  return None


def ParseRegion(region_node):
  (llab_node, lod_node) = kml.kmlparse.ParseRegion(region_node)
  llab = kml.kmlparse.ParseLatLonAltBox(llab_node)
  lod = kml.kmlparse.ParseLod(lod_node)
  return (llab, lod)


def GetNetworkLinkRegion(networklink_node):
  region_nodelist = networklink_node.getElementsByTagName('Region')
  if region_nodelist:
    return ParseRegion(region_nodelist[0])
  return (None, None)


# TODO 1) check Region hierarchy within file
# TODO 2) check Region hierarchy within children
def WalkNetworkLinks(kmlfile, parent_llab):
  print kmlfile
  global file_count
  file_count += 1

  # Sets the url to which all children are relative
  href = kml.href.Href()
  href.SetUrl(kmlfile)

  kp = kml.kmlparse.KMLParse(kmlfile)
  doc = kp.Doc()
  if not doc:
    print kmlfile,'load or parse error'
    return

  region_nodelist = doc.getElementsByTagName('Region')
  for region in region_nodelist:
    if not CheckRegion(region):
      print kmlfile,'bad Region'
    (llab, lod) = ParseRegion(region)
    if not CheckLatLonBoxContains(parent_llab, llab):
      print kmlfile,'child region not within parent'

  networklink_nodelist = doc.getElementsByTagName('NetworkLink')
  for networklink_node in networklink_nodelist:
    (llab,lod) = GetNetworkLinkRegion(networklink_node)
    # XXX assumes a relative href
    href.SetBasename(GetNetworkLinkFile(networklink_node))
    WalkNetworkLinks(href.Href(), llab)


WalkNetworkLinks(inputkml, None)

print 'checked %d regions in %d files, %d errors' % \
      (region_count,file_count,error_count)

