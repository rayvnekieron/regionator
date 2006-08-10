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



import sys

import kml.genkml
import kml.region

root = kml.region.Region(10,0,10,0,'0')
ne = root.Region('01')
sw = root.Region('02')
se = root.Region('03')
sese = root.Region('033')
sesese = root.Region('0333')
sesesese = root.Region('03333')
maxdepth = sesesese.Depth()

def DepthScale(d,max):
  return kml.region.Breadth(max - d + 1) * 8

def DepthName(d):
  return 'gridso%02d.jpg' % d

_kml = []
_kml.append(kml.genkml.KML21())
_kml.append('<Document>\n')

(x,y) = root.Grid()
d = root.Depth()
img = DepthName(d)
s = DepthScale(d,maxdepth)
_kml.append(kml.genkml.ScreenOverlay('root', img, d, s*x, s*y, s, s))

(x,y) = ne.Grid()
d = ne.Depth()
img = DepthName(d)
s = DepthScale(d,maxdepth)
_kml.append(kml.genkml.ScreenOverlay('ne', img, d, s*x, s*y, s, s))

(x,y) = sw.Grid()
d = sw.Depth()
img = DepthName(d)
s = DepthScale(d,maxdepth)
_kml.append(kml.genkml.ScreenOverlay('sw', img, d, s*x, s*y, s, s))

(x,y) = se.Grid()
d = se.Depth()
img = DepthName(d)
s = DepthScale(d,maxdepth)
_kml.append(kml.genkml.ScreenOverlay('se', img, d, s*x, s*y, s, s))

(x,y) = sese.Grid()
d = sese.Depth()
img = DepthName(d)
s = DepthScale(d,maxdepth)
_kml.append(kml.genkml.ScreenOverlay('sese', img, d, s*x, s*y, s, s))

(x,y) = sesese.Grid()
d = sesese.Depth()
img = DepthName(d)
s = DepthScale(d,maxdepth)
_kml.append(kml.genkml.ScreenOverlay('sesese', img, d, s*x, s*y, s, s))

(x,y) = sesesese.Grid()
d = sesesese.Depth()
img = DepthName(d)
s = DepthScale(d,maxdepth)
_kml.append(kml.genkml.ScreenOverlay('sesesese', img, d, s*x, s*y, s, s))

_kml.append('</Document>\n')
_kml.append('</kml>')

f = open('gridso.kml','w')
f.write("".join(_kml))
f.close()

