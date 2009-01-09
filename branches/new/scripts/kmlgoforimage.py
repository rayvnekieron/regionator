#!/usr/bin/env python

import sys
import kml.image
import kml.genkml

imagefile = sys.argv[1]
outputkml = sys.argv[2]

image = kml.image.Image(imagefile)
(n,s,e,w) = image.NSEW()
if not image.ValidNSEW():
  print 'Invalid bounding box',n,s,e,w
  sys.exit(1)

go = kml.genkml.GroundOverlay(n, s, e, w, imagefile, 0)

f = open(outputkml, 'w')
f.write(go)
f.close


