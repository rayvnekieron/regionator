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



# requires ImageMagick (convert)

import os
import sys

if len(sys.argv) != 3:
  print 'usage: %s basename maxdepth' % sys.argv[0]
  sys.exit(1)

basename = sys.argv[1]
maxdepth = int(sys.argv[2])

# as depth increases color goes from b->r
def DepthColor(depth,maxdepth):
  r = (depth * 255)/maxdepth
  b = 255 - r
  g = 0
  return (r,g,b)

def MakeColorFile(r,g,b,base,num):
  name = '%s%02d.jpg' % (base,num+1)
  print name
  cmd = 'convert -size 32x32 \'xc:rgb(%d,%d,%d)\' %s' % (r,g,b,name)
  os.system(cmd)

def MakeColorFiles(basename,maxdepth):
  d = 0
  while d < maxdepth:
    (r,g,b) = DepthColor(d, maxdepth)
    MakeColorFile(r,g,b,basename,d)
    d += 1

MakeColorFiles(basename,maxdepth)

