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


"""

KMZ utilities

"""

import zipfile
import os


def Extract(zipfilename, dir):

  """ KMZ extract to 'dir'

  Args:
    zipfilename: input .zip/.kmz file
    dir: output directory

  Returns:
    namelist: list of files in .zip/.kmz file
  """

  if not zipfile.is_zipfile(zipfilename):
    print 'ZipExtract: %s not a zipfile' % zipfilename
    return None

  zfd = zipfile.ZipFile(zipfilename)
  namelist = zfd.namelist()

  # print 'ZipExtract: extracting %d files into %s' % (len(namelist), dir)
  for name in namelist:
    # print name
    data = zfd.read(name)
    outname = os.path.join(dir, name)
    odir = os.path.dirname(outname)
    if not os.path.exists(odir):
      os.makedirs(odir, mode=0755)
    f = open(outname, 'w')
    f.write(data)
    f.close

  return namelist


def Create(zipfilename, namelist, dir):

  """ KMZ create from dir

  Args:
    zipfilename: .zip/.kmz file to create
    namelist: list of filenames to archive
    dir: directory of files

  """

  zfd = zipfile.ZipFile(zipfilename, mode = 'w', compression = zipfile.ZIP_DEFLATED)

  for name in namelist:
    fromname = os.path.join(dir,name)
    # print '%s -> %s' % (fromname, name)
    zfd.write(fromname, name)

def RmMinusR(dir):

  """ rm -rf dir

  Remove the directory and everything beneath

  Args:
    dir: remove this directory and evert

  """

  for (dirpath, dirnames, filenames) in os.walk(dir, topdown=False):
    for filename in filenames:
      path = os.path.join(dirpath, filename)
      # print 'Removing',path
      os.remove(path)
    # print 'Removing',dirpath
    os.rmdir(dirpath)

