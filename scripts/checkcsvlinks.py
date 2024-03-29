#!/usr/bin/env python

"""
Copyright (C) 2007 Google Inc.

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


# Check all link targets in a CSV file

import sys
import kml.checklinks

if len(sys.argv) < 2:
  print 'usage: %s [-h] [-a] [-r] [-v] [-s] [-c] -u file.csv' % sys.argv[0]
  print '   -h: check HTML hrefs'
  print '   -a: check absolute URLs'
  print '   -r: check relative URLs'
  print '   -c: compute checksum'
  print '   -v: verbose'
  print '   -s: print summary only'
  print '   -u file.csv: CSV to check'
  sys.exit(1)

status = kml.checklinks.CheckCsvLinks(sys.argv[1:])

if status == -1:
  print 'CSV file bad'

sys.exit(status)
