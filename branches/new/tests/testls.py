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

import kml.linestringregionator
import kml.qidboxes

kmlfile = sys.argv[1]
rootfile = sys.argv[2]
dir = sys.argv[3]

minpx = 384
minfade = 128
maxfade = 0
# a number made up for testing...
per = 15

lsr = kml.linestringregionator.LineStringRegionator()
lsr.SetFade(minfade,maxfade)
rtor = lsr.Regionate(kmlfile,minpx,per,rootfile,dir)
qidboxes = os.path.join(dir, 'qidboxes.kml')
kml.qidboxes.MakeQidBoxes(rtor, qidboxes)


