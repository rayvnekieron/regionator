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



# Test of some Region methods.

import kml.region
import kml.genkml
import kml.genxml

print 'region Region start...'

r = kml.region.Region(20,10,40,20,'0')
print '0 ',r.NSEW()
if r.Qid() != '0':
  print 'ERROR: region Region Qid() failed',r.Qid()
if r.Depth() != 1:
  print 'ERROR: region Region Depth() failed',r.Depth()

for q in ['0','1','2','3']:
  rc = r.Child(q)
  qid = '0' + q
  if rc.Qid() != qid:
    print 'ERROR: region Region qid() failed',rc.Qid()
  if rc.Depth() != 2:
    print 'ERROR: region Region Depth() failed',rc.Depth()

for q in ['0','1','2','3']:
  rc = r.Child(q)
  print '0' + q,rc.NSEW()

region = kml.region.Region(30,10,40,20,'0')

region012 = region.Region('012')
print region012.NSEW()

region000 = region.Region('000')
if region000.NSEW() != (30,25,25,20):
  print 'ERROR: kml.region.Region()',region000.NSEW()

region033 = region.Region('033')
if region033.NSEW() != (15,10,40,35):
  print 'ERROR: kml.region.Region()',region033.NSEW()


root = kml.region.RootRegion()
n = 21.2
s = 19.5
e = -115.4
w = -117.5
r = root.Snap(n,s,e,w)
(_n,_s,_e,_w) = r.NSEW()
print 'orig',n,s,e,w
print r.Qid(),_n,_s,_e,_w

document = kml.genxml.Document()
node = r.Qid()
d = 1
while d <= r.Depth():
  qid = node[0:d]
  _r = root.Region(qid)
  (_n,_s,_e,_w) = _r.NSEW()
  document.Add_Feature(kml.genkml.LatLonOutline(_n,_s,_e,_w,qid))
  d += 1

document.Add_Feature(kml.genkml.LatLonOutline(n,s,e,w,'orig'))

k = kml.genxml.Kml()
k.Feature = document.xml()

f = open('ancestors.kml','w')
f.write(k.xml())
f.close

r = kml.region.Region(20,10,50,40,'0')

nw = kml.region.Location('0')
print 'nw','0',nw
if nw != (0,1):
  print 'ERROR nw kml.region.Location()'

ne = kml.region.Location('1')
print 'ne','1',ne
if ne != (1,1):
  print 'ERROR ne kml.region.Location()'
sw = kml.region.Location('2')

print 'sw','2',sw
if sw != (0,0):
  print 'ERROR sw kml.region.Location()'
se = kml.region.Location('3')

print 'se','3',se
if se != (1,0):
  print 'ERROR se kml.region.Location()'

n00 = kml.region.Grid('00')
n01 = kml.region.Grid('01')
n02 = kml.region.Grid('02')
n03 = kml.region.Grid('03')
n000 = kml.region.Grid('000')

n03 = kml.region.Grid('03')
if n03 != (1,0):
  print 'ERROR n03 kml.region.Grid()'

n033 = kml.region.Grid('033')
if n033 != (3,0):
  print 'ERROR n033 kml.region.Grid()',n033

n0333 = kml.region.Grid('0333')
if n0333 != (7,0):
  print 'ERROR n0333 kml.region.Grid()',n0333

n0312312 = kml.region.Grid('0312312')
n0333333 = kml.region.Grid('0333333')
print '0312312',n0312312
print '0333333',n0333333

root = kml.region.RootRegion()
kml_lon = -122.082163
kml_lat =   37.420422
max_depth = 18
print 'SnapPoint',kml_lon,kml_lat
ra = root.SnapPoint(kml_lon, kml_lat, max_depth)
rb = kml.region.RootSnapPoint(kml_lon, kml_lat, max_depth)
if ra.NSEW() != rb.NSEW():
  print 'ERROR RootSnap failed'
print ra.Depth(), ra.Qid()
if ra.Depth() != max_depth:
  print 'ERROR RootSnapPoint failed'

print 'region Region ...end'
