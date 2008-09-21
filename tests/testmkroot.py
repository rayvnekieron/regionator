#!/usr/bin/env python

import kml.region
import kml.regionator

rootkml = 'root.kml'
region = kml.region.Region(2,1,4,3,'0')
lod = 128
dir = 'foo'
kml.regionator.MakeRootKML(rootkml,region,lod,dir)

