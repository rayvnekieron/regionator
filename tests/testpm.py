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
import os

import kml.placemarkregionator
import kml.region
import kml.qidboxes
import kml.dashboard

if sys.argv.__len__() != 4:
	print 'usage: %s placemarks.kml root.kml dir' % sys.argv[0]

kmlfile = sys.argv[1]
topfile = sys.argv[2]
dir = sys.argv[3]
boxfile = os.path.join(dir, 'qidboxes.kml')

minpx = 128
maxpx = -1
# intentionally low to deepen the hierarchy for testing
per = 7 # (42/2)/3

pmr = kml.placemarkregionator.PlacemarkRegionator()
rtor = pmr.Regionate(kmlfile,minpx,per,topfile,dir)
kml.qidboxes.MakeQidBoxes(rtor,boxfile)

imgbase = 'color'
fmt = 'jpg'
dbfile = os.path.join(dir, 'db.kml')
kml.dashboard.MakeDashBoard(rtor,imgbase,fmt,dbfile)

