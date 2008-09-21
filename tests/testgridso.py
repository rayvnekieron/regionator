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

import kml.genkml
import kml.genxml
import kml.region

root = kml.region.Region(10,0,10,0,'0')
root.SetId('root')
ne = root.Region('01')
ne.SetId('ne')
sw = root.Region('02')
sw.SetId('sw')
se = root.Region('03')
se.SetId('se')
sese = root.Region('033')
sese.SetId('sese')
sesese = root.Region('0333')
sesese.SetId('sesese')
sesesese = root.Region('03333')
sesesese.SetId('sesesese')
maxdepth = sesesese.Depth()


document = kml.genxml.Document()

def Add_ScreenOverlay(region):
  name = region.Id()
  (x,y) = region.Grid()
  d = region.Depth()
  s = kml.region.DepthScale(d,maxdepth)
  (b,g,r) = kml.region.DepthColor(d,maxdepth)
  color = 'ff%02x%02x%02x' % (b,g,r)
  so = kml.genkml.ScreenOverlayRect(name, color, d, s*x, s*y, s, s)
  document.Add_Feature(so)

for r in [root, ne, sw, se, sese, sesese, sesesese]:
  Add_ScreenOverlay(r)

k = kml.genxml.Kml()
k.Feature = document.xml()

f = open('gridso.kml','w')
f.write(k.xml())
f.close()

