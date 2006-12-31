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
import kml.walk
import os.path


if len(sys.argv) != 2:
  print 'usage: %s input.kml' % sys.argv[0]
  sys.exit(1)

inputkml = sys.argv[1]

region_count = 0
file_count = 0
error_count = 0


def CheckLatLonBoxSize(name, llb):
  global error_count
  status = True
  if float(llb.north) - float(llb.south) < .0001:
    print name,'bbox too short',llb.north,llb.south
    error_count += 1
    status = False
  if float(llb.east) - float(llb.west) < .0001:
    print name,'bbox too narrow',llb.east,llb.west
    error_count += 1
    status = False
  return status


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
    if float(llab.minAltitude) > float(llab.maxAltitude):
      error_count += 1
      print 'minAltitude less than maxAltitude'
      status = False
  if not CheckLatLonBoxSize('LatLonAltBox', llab):
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


def ParseRegion(region_node):
  (llab_node, lod_node) = kml.kmlparse.ParseRegion(region_node)
  llab = kml.kmlparse.ParseLatLonAltBox(llab_node)
  lod = kml.kmlparse.ParseLod(lod_node)
  return (llab, lod)


class CheckRegionNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self):
    self.__file_count = 0
    self.__region_count = 0

  def HandleNode(self, href, node, llab, lod):
    self.__file_count += 1
    region_nodelist = node.getElementsByTagName('Region')
    for region in region_nodelist:
      self.__region_count += 1
      if not CheckRegion(region):
        print 'bad Region'
      (llab, lod) = ParseRegion(region)
      if not CheckLatLonBoxContains(llab, llab):
        print 'child region not within parent'

  def PrintSummary(self):
    print 'checked %d regions in %d files, %d errors' % \
      (self.__region_count,self.__file_count,error_count)


check_region_node_handler = CheckRegionNodeHandler()
hierarchy = kml.walk.KMLHierarchy()
hierarchy.SetNodeHandler(check_region_node_handler)
hierarchy.SetVerbose(True)
hierarchy.Walk(inputkml, None, None)
check_region_node_handler.PrintSummary()

