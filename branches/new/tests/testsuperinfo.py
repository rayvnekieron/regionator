#!/usr/bin/env python

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



import sys
import os

import kml.image
import kml.superoverlayinfo
import kml.superoverlaypoly
import kml.tile

av0 = sys.argv[0]
argc = sys.argv.__len__()
if argc != 4 and argc != 8:
        print 'usage: %s imagefile tiles.txt dir [n s e w]' % av0
        sys.exit(1)


imagefile = sys.argv[1]
tilefile = sys.argv[2]
dir = sys.argv[3]
if argc == 8:
        north = float(sys.argv[4])
        south = float(sys.argv[5])
        east = float(sys.argv[6])
        west = float(sys.argv[7])

if dir != '-':
  os.makedirs(dir)

image = kml.image.Image(imagefile)
if argc == 8:
  image.SetNSEW(north,south,east,west)

twid = 512
tht = 512

# init...
superoverlayinfo = kml.superoverlayinfo.SuperOverlayInfo(image,twid,tht)
rtor = superoverlayinfo.Regionate()
maxdepth = rtor.MaxDepth()
print 'maxdepth',maxdepth
print 'count',rtor.RegionCount()
rootregion = superoverlayinfo.RootRegion()
print 'root region',rootregion.NSEW()
tiles = superoverlayinfo.Tiles()

# purposely cleanroom implementation
def CheckTile(image,tile):
  (tn,ts,te,tw) = tile.NSEW()
  (n,s,e,w) = image.NSEW()
  if tn > n or ts < s or te > e or tw < w:
    print '%s: ERROR tile llb out of bounds' % av0
  
  (x,y,twid,tht) = tile.Info()
  (wid,ht) = image.Dimensions()

  if x < 0 or x + twid > wid:
    print '%s: ERROR tile x out of bounds: %f + %f > %f' % (av0,x,twid,wid)
  if y < 0 or y + tht > ht:
    print '%s: ERROR tile y out of bounds: %f + %f > %f' % (av0,y,tht,ht)

f = open(tilefile,'w')
for qid in tiles.keys():
  tile = tiles[qid]
  CheckTile(image,tile)
  (x,y,wid,ht) = tile.Info()
  (n,s,e,w) = tile.NSEW()
  str = '%s %f %f %f %f %f %f %f %f\n' % (qid,x,y,wid,ht,n,s,e,w)
  f.write(str)
f.close()

if dir != '-':
  superoverlaypoly = kml.superoverlaypoly.SuperOverlayPoly(rootregion,tiles,maxdepth,dir)
  superoverlaypoly.Regionate()

