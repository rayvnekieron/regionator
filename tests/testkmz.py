#!/usr/bin/python

import sys
import tempfile

import kml.kmz

kmzin = sys.argv[1]
kmzout = sys.argv[2]

dir = tempfile.mkdtemp()

namelist = kml.kmz.Extract(kmzin, dir)
kml.kmz.Create(kmzout, namelist, dir)
kml.kmz.RmMinusR(dir)
