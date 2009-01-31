#!/usr/bin/python
# Check if the gdal module is present.
# Exit with 0 if it is or with 1 if it is not.

import sys

try:
 import gdal
except:
 print 'NO gdal'
 sys.exit(1)

print 'HAVE gdal'
sys.exit(0)
