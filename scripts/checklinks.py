#!/usr/bin/python

# Check all link targets in a KML file/hierarchy.

import sys
import kml.checklinks

if len(sys.argv) < 2:
  print 'usage: %s [-k] [-h] [-a] [-r] [-v] [-s] [-c] [-e encoding] url.kml' \
                                                                  % sys.argv[0]
  print '   -k: check KML hrefs'
  print '   -h: check HTML hrefs'
  print '   -a: check absolute URLs'
  print '   -a: check relative URLs'
  print '   -c: compute checksum'
  print '   -v: verbose'
  print '   -s: print summary only'
  print '   -e encoding: override xml encoding'
  sys.exit(1)

inputkml = sys.argv[len(sys.argv)-1]

status = kml.checklinks.CheckLinks(sys.argv[1:], inputkml)

if status == -1:
  print '%s: not found or failed parse' % inputkml

sys.exit(status)
