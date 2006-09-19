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

import urllib

import sys

import kml.wms
import kml.genxml

terra_url='http://terraservice.net/ogcmap.ashx?VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:4326&WIDTH=256&HEIGHT=256&LAYERS=DRG,DRG,DRG&STYLES=GeoGrid_Red,GeoGrid_Red,GeoGrid_Red&TRANSPARENT=FALSE&FORMAT=image/jpeg&'

region_w = kml.region.Region(40,39.9,-100,-100.1,'0')
region_e = kml.region.Region(40,39.9,-99.9,-100,'0')

wmskml = 'terra.kml'

def EntityAmp(str):
  n = []
  ss = str.split('&')
  for s in ss:
    n.append(s)
    n.append('&amp;')
  return "".join(n)

def GO(wmsurl,region,draworder,filename):
  url = wmsurl + kml.wms.WMSBBOX(region)
  u = urllib.urlopen(url)
  buf = u.read()
  f = open(filename, 'w')
  f.write(buf)
  f.close()
  u.close()

  (n,s,e,w) = region.NSEW()
  return kml.genkml.GroundOverlay(n,s,e,w,filename,0)
  

document = kml.genxml.Document()

styleid = 'radiostyle'
style = kml.genxml.Style()
style.id = styleid
style.ListStyle = kml.genkml.ListStyle('radioFolder')
document.Add_Style(style.xml())
document.styleUrl = '#%s' % styleid

# Earth does WMS load

f0 = kml.genxml.Folder()
f0.name = 'WMS'
f0.Add_Feature(kml.wms.WMSGroundOverlay(EntityAmp(terra_url), region_w, 0))
f0.Add_Feature(kml.wms.WMSGroundOverlay(EntityAmp(terra_url), region_e, 0))

# This script does WMS load to local file for Earth to show

f1 = kml.genxml.Folder()
f1.name = 'local image'
f1.Add_Feature(GO(terra_url,region_w,0,'terra_w.jpg'))
f1.Add_Feature(GO(terra_url,region_e,0,'terra_e.jpg'))

document.Add_Feature(f0.xml())
document.Add_Feature(f1.xml())

k = kml.genxml.Kml()
k.Feature = document.xml()

f = open(wmskml, 'w')
f.write(k.xml())
f.close()

