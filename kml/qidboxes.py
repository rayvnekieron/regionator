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

""" MakeQidBoxes()

Builds a single flat KML file of one Placemark LineString
with the Region for each qid in the given regionator's qid list.
Use on a kml.regionator.Regionator()-derived class after Regionate().

Principally for debugging purposes: permits a tour of a given
dataset's Regions.

"""

import kml.regionator
import kml.genkml


def MakeQidBoxes(rtor,boxfile):

  """
  Creates a single KML document of Region boxes (LineStrings).

  Args:
    boxfile: file to write the KML document
  """

  _kml = []
  _kml.append(kml.genkml.KML21())
  _kml.append('<Document>\n')
  rootregion = rtor.RootRegion()

  qids = rtor.QidList()
  for qid in qids:
    _kml.append('\n<Placemark>')
    _kml.append('<name>qid %s</name>\n' % qid)
    r = rootregion.Region(qid)
    (n,s,e,w) = r.NSEW()
    (minpx,maxpx) = rtor.LodPixels(r)
    _kml.append(kml.genkml.Region(n,s,e,w,minpx=minpx,maxpx=maxpx))
    _kml.append(kml.genkml.LineStringBox(n,s,e,w))
    _kml.append('\n')
    _kml.append('</Placemark>\n')

  _kml.append('</Document>\n')
  _kml.append('</kml>\n')

  f = open(boxfile,'w')
  f.write("".join(_kml))
  f.close()

