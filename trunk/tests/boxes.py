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



# Simple test program to draw a box (LineString) for
# each Region as specifed.
# Helps visualize the location and depth of Regions and 
# the effect of the specified lods.

import sys
import os

import kml.region
import kml.regionhandler
import kml.regionator
import kml.genkml
import kml.dashboard

if len(sys.argv) != 9:
  print 'usage: %s dir n s e w minpx maxpx depth' % sys.argv[0]
  sys.exit(1)


dir = sys.argv[1]
n = float(sys.argv[2])
s = float(sys.argv[3])
e = float(sys.argv[4])
w = float(sys.argv[5])
minpx = int(sys.argv[6])
maxpx = int(sys.argv[7])
maxdepth = int(sys.argv[8])
minfade = 128
maxfade = 128

qid = '0'

os.makedirs(dir)


class BoxRegionHandler(kml.regionhandler.RegionHandler):

  def Start(self,region):
    if region.Depth() > maxdepth:
      return [False,False]# no data here or below
    return [True,True] # yes, have data here, and maybe below too

  def Data(self,region):
    qid = region.Qid()
    (n,s,e,w) = region.NSEW()
    return kml.genkml.Box(n,s,e,w,qid)

  def PixelLod(self,region):
    return (minpx,maxpx)

myregionator = kml.regionator.Regionator()
myregionator.SetRegionHandler(BoxRegionHandler())
myregionator.SetOutputDir(dir)
region = kml.region.Region(n,s,e,w,qid)
myregionator.SetFade(minfade,maxfade)
myregionator.Regionate(region)

dbfile = os.path.join(dir, 'db.kml')
kml.dashboard.MakeDashBoard(myregionator, dbfile)

