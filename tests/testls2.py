#!/usr/bin/env python

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

import sys
import os

import kml.kmlregionator
import kml.regionator
import kml.qidboxes

if len(sys.argv) != 4:
  print 'usage: %s linestrings.kml root.kml dir' % sys.argv[0]
  sys.exit(1)

lskml = sys.argv[1]
rootkml = sys.argv[2]
dir = sys.argv[3]

if not os.path.exists(dir):
  os.makedirs(dir)

def RegionateLineStrings(lskml, rootfile, dir):

  """Sort input LineStrings into a Region-based NetworkLink hierarchy

  Args:
    lskml: KML file of LineString's
    rootfile: output root of RbNL hierarchy
    dir: directory of RbNL KML files
  """


  kml_parse = kml.kmlparse.KMLParse(lskml)

  # The generic KML regionator finds the LineStrings in kml_parse,
  # sorts on size (footprint) and buckets "max_per" LineStrings per Region,
  # and sets the LOD of each Region as specified.
  min_lod_pixels = 384
  max_per = 15
  kml_region_handler = kml.kmlregionator.KMLRegionHandler(kml_parse,
                                                          min_lod_pixels,
                                                          max_per)


  # Create a regionator instance and plug in the kml regionator.
  rtor = kml.regionator.Regionator()
  rtor.SetRegionHandler(kml_region_handler)

  # Specify the given fade range.
  minfade = 128
  maxfade = 0  # maxLodPixels == -1 so maxFadeExtent has no meaning
  rtor.SetFade(minfade,maxfade)

  # Specify where to save the KML hierarchy.
  rtor.SetOutputDir(dir)

  # Inquire the bounding box of the set of all input LineStrings
  # and align the native region hierarchy.
  (n,s,e,w) = kml_region_handler.NSEW()
  region = kml.region.RootSnap(n,s,e,w)

  # Visit every region and generate KML.
  rtor.SetVerbose(False)  # Default is True
  rtor.Regionate(region)

  # Write out a root KML file to point to the RbNL hierarchy in dir.
  kml.regionator.MakeRootKML(rootkml, region, min_lod_pixels, dir)

  # Generate a debugging set of (Region LineString) boxes.
  qidboxes = os.path.join(dir, 'qidboxes.kml')
  kml.qidboxes.MakeQidBoxes(rtor, qidboxes)


RegionateLineStrings(lskml, rootkml, dir)


