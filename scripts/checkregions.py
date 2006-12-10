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
import os.path


if len(sys.argv) != 2:
  print 'usage: %s input.kml' % sys.argv[0]
  sys.exit(1)

inputkml = sys.argv[1]


def CheckLatLonBox(name, llb):
  status = True
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
  if lod.maxLodPixels == None or lod.maxLodPixels == -1:
    return status

  if lod.minLodPixels <= lod.maxLodPixels:
    print 'Lod: minLodPixels not greater than maxLodPixels'
    status = False
  return status


def CheckRegion(region_node):
  print 'Region',
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


def WalkNetworkLinks(kmlfile):
  # XXX presumes kmlfile is a _file_...
  print kmlfile
  kp = kml.kmlparse.KMLParse(kmlfile)
  doc = kp.Doc()
  region_nodelist = doc.getElementsByTagName('Region')
  for region in region_nodelist:
    if not CheckRegion(region):
      if verbose:
        print kmlfile,'bad Region'
  networklink_nodelist = doc.getElementsByTagName('NetworkLink')
  for networklink_node in networklink_nodelist:
    linkfile = GetNetworkLinkFile(networklink_node)
    fullname = RelativeName(kmlfile, linkfile)
    WalkNetworkLinks(fullname)


WalkNetworkLinks(inputkml)



