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

""" MakeDashBoard()

Region-triggered ScreenOverlays

"""

import kml.regionator
import kml.genkml

def DepthScale(d,max):
  return kml.region.Breadth(max - d + 1) * 8

# as depth increases color goes from b->r
def DepthColor(depth,maxdepth):
  r = (depth * 255)/maxdepth
  b = 255 - r
  g = 0
  return (b,g,r)

def MakeDashBoard(rtor, dbfile):

  """
  Builds a single flat KML file of one ScreenOverlay per Region
  Use on a kml.regionator.Regionator()-derived class after Regionate().

  Args:
    rtor: kml.regionator.Regionator() post Regionate()
    dbfile: file to write the KML document
  """

  _kml = []
  _kml.append(kml.genkml.KML21())
  _kml.append('<Document>\n')
  rootregion = rtor.RootRegion()
  maxdepth = rtor.MaxDepth()

  qids = rtor.QidList()
  for qid in qids:
    r = rootregion.Region(qid)
    (n,s,e,w) = r.NSEW()
    (minpx,maxpx) = rtor.LodPixels(r)
    kmlregion = kml.genkml.Region(n,s,e,w,minpx=minpx,maxpx=maxpx)

    depth = r.Depth()
    (x,y) = r.Grid()
    s = DepthScale(depth,maxdepth)

    color = 'ff%02x%02x%02x' % DepthColor(depth,maxdepth)
    _kml.append(kml.genkml.ScreenOverlayRect(qid,color,depth,s*x,s*y,s,s,kmlregion))
    _kml.append('\n')

  _kml.append('</Document>\n')
  _kml.append('</kml>\n')

  f = open(dbfile,'w')
  f.write("".join(_kml))
  f.close()

