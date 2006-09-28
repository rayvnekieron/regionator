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

import kml.superoverlay

argc = len(sys.argv)
if argc != 4 and argc != 5:
  print 'usage: %s image.gtif root.kml dir' % sys.argv[0]
  print 'usage: %s imagefile go.kml root.kml dir' % sys.argv[0]
  sys.exit(1)

imagefile = sys.argv[1]

if argc == 5:
  gokml = sys.argv[2]
  root = sys.argv[3]
  dir = sys.argv[4]
  kml.superoverlay.SuperOverlay(imagefile, root, dir, gofile=gokml)
else:
  root = sys.argv[2]
  dir = sys.argv[3]
  kml.superoverlay.SuperOverlay(imagefile, root, dir)
