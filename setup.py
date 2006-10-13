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

import os
import distutils.core

def SVNVersion():
  svnversioncmd = os.popen('svnversion -n .')
  svnversion = svnversioncmd.read()

  f = open('kml/svnversion.py','w')
  f.write('svnversion = "%s"\n' % svnversion)
  f.close()
  return svnversion

script_list = [
  'scripts/superoverlay.py',
  'scripts/placemarks.py',
  'scripts/cgiregionator.py', # really for /var/www/cgi-bin or equiv
  'scripts/insertregions.py'
]

distutils.core.setup(name='kml',
  version='%s' % SVNVersion(),
  description='KML Regionator',
  packages=['kml'],
  scripts=script_list
)

