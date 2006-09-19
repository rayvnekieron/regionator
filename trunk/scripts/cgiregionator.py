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



# CGI-serve all Regions on Earth.

import os
import socket
import cgi
import sys

import kml.region
import kml.cgiregion
import kml.genkml
import kml.genxml

hostname=socket.gethostname()
script=os.path.basename(sys.argv[0])

baseurl='http://%s/cgi-bin/%s' % (hostname,script)


def CGIRegionate(region):

  # Find out what Region we are serving
  # and if we have child Regions

  (n,s,e,w) = region.NSEW()

  # Cannot bound maxLodPixels of the NetworkLink hierarchy
  # as the viewpoint can travel through the Region before
  # it triggers.
  # Cannot set minLodPixels too low or the client floods
  # the server with onRegion requests on any small viewpiont change.
  minpx = 128
  maxpx = -1

  document = kml.genxml.Document()
  document.name = region.Qid()

  style = kml.genxml.Style()
  styleid = 'mystyle'
  style.id = styleid
  a = 127
  b = 127
  g = 127
  r = 127
  style.LineStyle = kml.genkml.LineStyle(a,b,g,r)

  document.Region = kml.genkml.Region(n,s,e,w,minpx=minpx,maxpx=maxpx)

  children = kml.cgiregion.GetChildren(region)
  for q in children:
    document.Add_Feature(kml.cgiregion.LinkChild(baseurl,region,q,minpx,maxpx))

  placemark = kml.genxml.Placemark()
  placemark.styleUrl = '#%s' % styleid
  placemark.Geometry = kml.genkml.LineStringBox(n,s,e,w)

  document.Add_Feature(placemark.xml())

  k = kml.genxml.Kml()
  k.Feature = document.xml()
  return k.xml()


def SendKML(_kml):
  print 'Content-type: text/plain'
  print
  print _kml


fs = cgi.FieldStorage()
region = kml.cgiregion.Parse(fs)
if not region:
  region = kml.region.RootRegion()
_kml = CGIRegionate(region)
SendKML(_kml)
