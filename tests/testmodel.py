#!/usr/bin/python

import sys

import kml.kmlparse
import kml.genxml

if len(sys.argv) != 2:
  print 'usage: %s model.kml' % sys.argv[0]
  sys.exit(1)

modelkml = sys.argv[1]

kp = kml.kmlparse.KMLParse(modelkml)
location = kp.ExtractLocation()
orientation = kp.ExtractOrientation()
scale = kp.ExtractScale()

model = kml.genxml.Model()
model.Location = location.xml()
model.Orientation = orientation.xml()
model.Scale = scale.xml()
print model.xml()


