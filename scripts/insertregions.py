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
import xml.dom.minidom

import kml.kmlparse
import kml.coordbox
import kml.genkml

"""
for each <Folder>

  get items with <coordinates>

  find bounding box of items

  create a <Region>

  insert <Region> (and <LineString> box) into <Folder>


create a separate regions <Folder>

  for each <Region>

    add a <LineString>

"""

# xml.dom.minidom.import node not in 2.2
def PyVersionOK():
  v = sys.version.split() # split on space
  v = v[0].split('.')
  if v[0] >= '2' and v[1] >= '3':
    return True
  return False

if not PyVersionOK():
  print '%s: requires Python 2.3 or later' % sys.argv[0]
  sys.exit(1)

if len(sys.argv) != 3:
  print 'usage: %s input.kml output.kml' % sys.argv[0]
  sys.exit(1)

kmlin = sys.argv[1]
kmlout = sys.argv[2]

def MakeRegionDoc(n,s,e,w):
  regionkml = kml.genkml.RegionLod(n,s,e,w,128,-1)
  return xml.dom.minidom.parseString(regionkml)

def MakeBoxDoc(n,s,e,w):
  name = '%f %f %f %f' % (n,s,e,w)
  boxkml = kml.genkml.Box(n,s,e,w,name)
  return xml.dom.minidom.parseString(boxkml)

def DoPlacemark(placemark,cbox):
  coords = placemark.getElementsByTagName('coordinates')
  for coord in coords: # MultiGeometry...
    ctext = kml.kmlparse.GetText(coord)
    cbox.AddCoordinates(ctext)

def DoFolder(folder):
  cbox = kml.coordbox.CoordBox()
  pmcount = 0
  for child in folder.childNodes:
    if child.nodeType == child.ELEMENT_NODE:
      if child.localName == 'name':
        print 'Folder',kml.kmlparse.GetText(child).encode('utf-8'), # no newline
      elif child.localName == 'Placemark':
        DoPlacemark(child,cbox)
        pmcount = pmcount + 1
  # XXX if pmcount < 2 skip the Region...?
  if pmcount:
    (n,s,e,w) = cbox.NSEW()
    rdoc = MakeRegionDoc(n,s,e,w)
    bdoc = MakeBoxDoc(n,s,e,w)
    return (rdoc,bdoc)
  return (None,None)

kp = kml.kmlparse.KMLParse(kmlin)
doc = kp.Doc()

folders = doc.getElementsByTagName('Folder')
numfolders = len(folders)
progress = 1
for folder in folders:
  if folder.hasChildNodes():
    print '%d/%d' % (progress,numfolders),
    progress += 1
    (rdoc,bdoc) = DoFolder(folder)
    if rdoc and bdoc:
      bnode = doc.importNode(bdoc.childNodes[0],True)
      rnode = doc.importNode(rdoc.childNodes[0],True)
      # XXX move to separate Folder, smaller lod...
      folder.insertBefore(bnode,folder.childNodes[0])
      folder.insertBefore(rnode,folder.childNodes[0])
    print # the newline we have not yet printed



f = open(kmlout,'w')
f.write(doc.toxml().encode('utf-8'))
f.close()

