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


def CheckLatLonBox(name, llb):
  status = True
  # These are _not_ the defaults
  # A common error is for 0 to be take as "not set" (or None)
  if llb.north == None:
    print 'north not set'
    llb.north = 0
  if llb.south == None:
    print 'south not set'
    llb.south = 0
  if llb.east == None:
    print 'east not set'
    llb.east = 0
  if llb.west == None:
    print 'east not set'
    llb.west = 0
  if float(llb.north) <= float(llb.south):
    print '%s: north not greater than south' % name
    status = False
  if float(llb.east) <= float(llb.west):
    print '%s: east not greater than west' % name
    status = False
  return status


def CheckLatLonAltBox(llab):
  status = True
  if not CheckLatLonBox('LatLonAltBox', llab):
    status = False
  if llab.minAltitude and llab.maxAltitude:
    if float(llab.minAltitude) < float(llab.maxAltitude):
      print 'east not greater than west'
      status = False
  return status


def CheckLod(lod):
  status = True
  if lod.minLodPixels < 0:
    print 'Lod bad minLodPixels',lod.minLodPixels
    status = False
  if lod.maxLodPixels == None or float(lod.maxLodPixels) == -1:
    return status

  if float(lod.minLodPixels) > float(lod.maxLodPixels):
    print 'Lod: minLodPixels greater than maxLodPixels'
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
  link_nodelist = networklink_node.getElementsByTagName('Link')
  if link_nodelist:
    return GetLinkHref(link_nodelist[0])
  return None


def GetNetworkLinkRegion(networklink_node):
  region_nodelist = networklink_node.getElementsByTagName('Region')
  if region_nodelist:
    (llab_node, lod_node) = kml.kmlparse.ParseRegion(region_nodelist[0])
    llab = kml.kmlparse.ParseLatLonAltBox(llab_node)
    lod = kml.kmlparse.ParseLod(lod_node)
    return (llab, lod) # XXX
  return None


# TODO 1) check Region hierarchy within file
# TODO 2) check Region hierarchy within children
def WalkNetworkLinks(kmlfile):
  print kmlfile

  href = kml.href.Href()
  href.SetUrl(kmlfile)
  if href.GetScheme() == None:
    # Assume this is a local file
    kp = kml.kmlparse.KMLParse(kmlfile)
  else:
    # Assume http basically
    # XXX handle kmz
    data = kml.href.FetchUrl(kmlfile)
    kp = kml.kmlparse.KMLParse(None)
    kp.ParseString(data)
  doc = kp.Doc()

  region_nodelist = doc.getElementsByTagName('Region')
  for region in region_nodelist:
    if not CheckRegion(region):
      print kmlfile,'bad Region'
  networklink_nodelist = doc.getElementsByTagName('NetworkLink')
  for networklink_node in networklink_nodelist:
    linkfile = GetNetworkLinkFile(networklink_node)
    #fullname = RelativeName(kmlfile, linkfile)
    # XXX yuck

    linkhref = kml.href.Href()
    linkhref.SetUrl(linkfile)
    if linkhref.GetScheme():
      fullname = linkfile
    else:
      # Set the basename of the parent link to this child
      href.SetBasename(linkfile)
      fullname = href.Href()

    WalkNetworkLinks(fullname)


WalkNetworkLinks(inputkml)

print 'checked %d regions' % region_count

