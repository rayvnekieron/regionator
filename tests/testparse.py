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


import kml.kmlparse

print 'test kml.kmlparse.KMLParse go.kml ... start'

kmldoc = kml.kmlparse.KMLParse('go.kml')

latlonbox = kmldoc.ExtractLatLonBox()
if latlonbox.north != '20':
  print 'ERROR in ExtractLatLonBox'
if latlonbox.south != '-20':
  print 'ERROR in ExtractLatLonBox'
if latlonbox.east != '20':
  print 'ERROR in ExtractLatLonBox'
if latlonbox.west != '-20':
  print 'ERROR in ExtractLatLonBox'

#print latlonbox.xml()

icon = kmldoc.ExtractIcon()
if icon.href != 'foo.jpg':
  print 'ERROR in ExtractIcon'

# print icon.xml()

timespan = kmldoc.ExtractTimeSpan()
if timespan.begin != '2006':
  print 'ERROR in ExtractTimeSpan'
if timespan.end != '2007':
  print 'ERROR in ExtractTimeSpan'

# print timespan.xml()

go = kmldoc.ExtractGroundOverlay()
# print go.xml()
if go.drawOrder != '10':
  print 'ERROR in ExtractGroundOverlay'

print 'test kml.kmlparse.KMLParse go.kml ... done'

print 'test kml.kmlparse.KMLParse coit.kmz ... start'

kp = kml.kmlparse.KMLParse('coit.kmz')
location = kp.ExtractLocation()
if location.longitude != '-122.405843291645':
  print 'ERROR in KMZ parse',location.longitude
lookat = kp.ExtractLookAt()
if lookat.tilt != '49.82584784628866':
  print 'ERROR in KMZ parse',lookat.tilt

print 'test kml.kmlparse.KMLParse coit.kmz ... done'

print 'test kml.kmlparse.KMLParse region.kml ... start'

kp = kml.kmlparse.KMLParse('region.kml')
latlonaltbox = kp.ExtractLatLonAltBox()
if latlonaltbox.west != '-80.859375':
  print 'ERROR in ExtractLatLonAltBox.west'
if latlonaltbox.minAltitude != '100000':
  print 'ERROR in ExtractLatLonAltBox.minAltitude'
if latlonaltbox.maxAltitude != '100001':
  print 'ERROR in ExtractLatLonAltBox.maxAltitude'
if latlonaltbox.altitudeMode != 'absolute':
  print 'ERROR in ExtractLatLonAltBox.altitudeMode',latlonaltbox.altitudeMode

print 'test kml.kmlparse.KMLParse region.kml ... done'

print 'test kml.kmlparse.KMLParse ksc-llb-0.kml ... start'

kp = kml.kmlparse.KMLParse('ksc-llb-0.kml')
latlonaltbox = kp.ExtractLatLonAltBox()
if latlonaltbox:
  print 'ERROR in ExtractLatLonAltBox, no such expected'

print 'test kml.kmlparse.KMLParse ksc-llb-0.kml ... done'

