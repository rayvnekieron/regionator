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

"""

Dig out the .kml in a .kmz

"""

import sys
import os.path
import kml.kmlparse
import kml.genxml
import kml.href
import kml.kmz


argc = len(sys.argv)
if argc < 2 or argc > 3:
  print 'usage: %s input.kmz [output.kml]' % sys.argv[0]
  sys.exit(1)

inputkmz = sys.argv[1]
if argc == 3:
  outputkml = sys.argv[2]
else:
  outputkml = None

kmldata = kml.kmz.ExtractKMLFile(inputkmz)
if outputkml:
  f = open(outputkml,'w')
  f.write(kmldata)
  f.close()
else:
  print kmldata,
