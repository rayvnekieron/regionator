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

"""
Regionate pipe-delimited data, sorted by score.
The minimum supplied data are in this format:
score|lat|lon|name|description

Additionally, a 6th row may be supplied to define a <styleUrl>:
score|lat|lon|name|description|styleUrl

In this case, the styleUrl should use a relative href to point to a file at
the top-level of the generated directory structure, or should point to a kml
file over http.
"""

import os
import sys
import kml.csvregionator

if len(sys.argv) != 4:
  print 'usage: %s input.csv root.kml dir' % sys.argv[0]
  sys.exit(1)

csvfile = sys.argv[1]
codec = 'UTF-8'
min_lod = 256
max_per = 16
rootkml = sys.argv[2]
dir = sys.argv[3]
verbose = True
os.makedirs(dir)
rtor = kml.csvregionator.RegionateCSV(csvfile, codec, min_lod, max_per,
                                      rootkml, dir, verbose)
if not rtor:
  status = -1
else:
  status = 0
sys.exit(status)