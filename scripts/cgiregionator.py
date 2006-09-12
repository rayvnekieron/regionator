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

  _kml = []
  _kml.append(kml.genkml.KML21())
  _kml.append('<Document>\n')
  _kml.append('<name>%s</name>\n' % region.Qid())

  styleid = 'mystyle'
  _kml.append('<Style id=\"%s\">\n' % styleid)
  a = 127
  b = 127
  g = 127
  r = 127
  _kml.append(kml.genkml.LineStyle(a,b,g,r))
  _kml.append('</Style>\n')

  _kml.append('\n')
  _kml.append(kml.genkml.Region(n,s,e,w,minpx=minpx,maxpx=maxpx))

  children = kml.cgiregion.GetChildren(region)
  for q in children:
    _kml.append('\n')
    _kml.append(kml.cgiregion.LinkChild(baseurl,region,q,minpx,maxpx))


  _kml.append('\n')
  su = '#%s' % styleid
  _kml.append(kml.genkml.Box(n,s,e,w,region.Qid(),styleurl=su))
  _kml.append('\n')

  _kml.append('</Document>\n')
  _kml.append('</kml>\n')
  return "".join(_kml)

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
