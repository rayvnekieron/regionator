#!/usr/bin/python

# Check all Icon/href targets in a KML file/hierarchy.

import sys
import kml.checkimages

if len(sys.argv) < 2:
  print 'usage: %s [-a] [-r] [-v] url.kml' % sys.argv[0]
  print '   -r: check relative URLs'
  print '   -a: check absolute URLs'
  print '   -v: verbose'
  sys.exit(1)

inputkml = sys.argv[len(sys.argv)-1]

status = kml.checkimages.CheckImages(sys.argv[1:], inputkml)

sys.exit(status)
