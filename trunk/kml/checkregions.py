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

import getopt
import kml.kmlparse
import kml.walk

class RegionCheckingNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self, opts):
    self.__file_count = 0
    self.__region_count = 0
    self.__error_count = 0

    self.__verbose = False
    opts, args = getopt.getopt(opts, 'v')
    for o,a in opts:
      if o == '-v':
        self.__verbose = True

  def Status(self):
    return self.__error_count

  def Statistics(self):
    return (self.__region_count, self.__file_count, self.__error_count)

  def _Print(self, code, data, *more):
    if self.__verbose:
      print code,data,
      for m in more:
        print m,
      print # newline


  def PrintSummary(self):
    self._Print('Summary', 'regions', self.__region_count)
    self._Print('Summary', 'files', self.__file_count)
    self._Print('Summary', 'errors', self.__error_count)


  def CheckLatLonBoxSize(self, name, llb):
    errors = 0
    if float(llb.north) - float(llb.south) < .0001:
      self._Print('ERR', name,'bbox too short',llb.north,llb.south)
      errors += 1
    if float(llb.east) - float(llb.west) < .0001:
      self._Print('ERR', name,'bbox too narrow',llb.east,llb.west)
      errors += 1
    return errors


  def CheckLatLonBoxFloats(self, name, llb):
    errors = 0

    try:
      float(llb.north)
    except:
      self._Print('ERR', '%s: north float invalid' % name)
      errors += 1

    try:
      float(llb.south)
    except:
      self._Print('ERR', '%s: south float invalid' % name)
      errors += 1

    try:
      float(llb.east)
    except:
      self._Print('ERR', '%s: east float invalid' % name)
      errors += 1

    try:
      float(llb.west)
    except:
      self._Print('ERR', '%s: west float invalid' % name)
      errors += 1

    return errors

  def CheckLatLonBox(self, name, llb):
    errors = 0
    # These are _not_ the defaults
    # A common error is for 0 to be taken as "not set" (or None)
    if llb.north == None:
      self._Print('ERR', 'north not set')
      errors += 1
      llb.north = 0
    if llb.south == None:
      self._Print('ERR', 'south not set')
      errors += 1
      llb.south = 0
    if llb.east == None:
      self._Print('ERR', 'east not set')
      errors += 1
      llb.east = 0
    if llb.west == None:
      self._Print('ERR', 'east not set')
      errors += 1
      llb.west = 0

    fatalities = self.CheckLatLonBoxFloats(name, llb)
    if fatalities:
      # If any float was invalid just bug out
      return (errors, fatalities)
      
    if float(llb.north) <= float(llb.south):
      self._Print('ERR', '%s: north not greater than south' % name)
      errors += 1
    if float(llb.east) <= float(llb.west):
      self._Print('ERR', '%s: east not greater than west' % name)
      errors += 1

    return (errors, 0)


  def CheckLatLonAltBox(self, llab):
    (errors, fatalities) = self.CheckLatLonBox('LatLonAltBox', llab)
    if not fatalities:
      errors += self.CheckLatLonBoxSize('LatLonAltBox', llab)
    if llab.minAltitude and llab.maxAltitude:
      if float(llab.minAltitude) > float(llab.maxAltitude):
        self._Print('ERR', 'minAltitude less than maxAltitude')
        errors += 1
    return errors + fatalities


  def CheckLatLonBoxContains(self, parent_llb, child_llb):
    if parent_llb == None:
      return 0
    # XXX deal with missing north, etc
    if (float(parent_llb.north) >= float(child_llb.north) and
        float(parent_llb.south) <= float(child_llb.south) and
        float(parent_llb.east) >= float(child_llb.east) and
        float(parent_llb.west) <= float(child_llb.west)):
      return 0
    self._Print('ERR', 'child region not within parent')
    return 1


  def CheckLod(self, lod):
    errors = 0
    if lod.minLodPixels:
      if lod.minLodPixels < 0:
        self._Print('ERR', 'Lod bad minLodPixels',lod.minLodPixels)
        errors += 1

    if lod.maxLodPixels:
      if lod.maxLodPixels < 1:
        self._Print('ERR', 'Lod bad maxLodPixels',lod.maxLodPixels)
        errors += 1
  
    if lod.minLodPixels and lod.maxLodPixels:
      if float(lod.maxLodPixels) != -1 and \
         float(lod.minLodPixels) >= float(lod.maxLodPixels):
        self._Print('ERR', 'Lod: minLodPixels not less than maxLodPixels')
        errors += 1
    return errors


  def CheckRegion(self, region_node):
    (llab, lod) = kml.kmlparse.ParseRegion(region_node)
    self._Print('Region', llab.north, llab.south, llab.east, llab.west)
    self.__region_count += 1
    self.__error_count += self.CheckLatLonAltBox(llab)
    self.__error_count += self.CheckLod(lod)


  # kml.walk.KMLNodeHandler::HandleNode()
  def HandleNode(self, href, node, parent_llab, parent_lod):
    self._Print('URL',href.Href())
    self.__file_count += 1
    region_nodelist = node.getElementsByTagName('Region')
    for region in region_nodelist:
      self.__region_count += 1
      self.CheckRegion(region)
      (llab, lod) = kml.kmlparse.ParseRegion(region)
      self.__error_count += self.CheckLatLonBoxContains(parent_llab, llab)


def CheckRegions(opts, inputkml):
  region_checking_node_handler = RegionCheckingNodeHandler(opts)
  hierarchy = kml.walk.KMLHierarchy()
  hierarchy.SetNodeHandler(region_checking_node_handler)
  hierarchy.Walk(inputkml, None, None)
  region_checking_node_handler.PrintSummary()
  return region_checking_node_handler
