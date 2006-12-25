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
import kml.href


class Kmz:

  """ Convenience front-end to zipfile

  Fetches remote kmz into a local temp file.
  Handles all zipfile exceptions.

  """

  def __init__(self, kmz_url):
    self.__kmz_temp = None
    self.__zfd = None

    href = kml.href.Href()
    href.SetUrl(kmz_url)

    if href.GetScheme():
      # The KMZ must first be fetched
      self.__kmz_temp = kml.href.FetchUrlToTempFile(kmz_url)
      kmz_path = self.__kmz_temp
    else:
      kmz_path = kmz_url

    try:
      zfd = zipfile.ZipFile(kmz_path)
    except:
      self.__del__()

      return
    self.__zfd = zfd

  def __del__(self):
    if self.__zfd:
      self.__zfd.close()
    if self.__kmz_temp:
      os.unlink(self.__kmz_temp)

  def GetSize(self, name):

    """Returns file size

    Args:
      name: name of file in archive

    Returns:
      size: uncompressed size if name exists
      None: no such name exists in archive
    """

    try:
      info = self.__zfd.getinfo(name)
      size = info.file_size
    except:
      size = None
    return size

  def Read(self, name):

    """Returns file data

    Args:
      name: name of file in archive

    Returns:
      data: the contents of name if it exists
      None: no such name exists in archive
    """
    try:
      data = self.__zfd.read(name)
    except:
      data = None
    return data
    
   



def ZipOpen(zipfilename):

  if not zipfile.is_zipfile(zipfilename):
    print 'ZipExtract: %s not a zipfile' % zipfilename
    return None

  return zipfile.ZipFile(zipfilename)


def Extract(zipfilename, dir):

  """ KMZ extract to 'dir'

  Args:
    zipfilename: input .zip/.kmz file
    dir: output directory

  Returns:
    namelist: list of files in .zip/.kmz file
  """
  
  zfd = ZipOpen(zipfilename)
  if not zfd:
    return None
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


def ExtractKMLFile(kmzfile):

  """ Extract the KML file from the KMZ archive

  Args:
    kmzfile: .kmz file

  Returns:
    data: the contents of the kml file
  """

  zfd = ZipOpen(kmzfile)
  if zfd:
    namelist = zfd.namelist()
    for name in namelist:
      if name.endswith('.kml'):
        data = zfd.read(name)
        return data
  return None


def Create(zipfilename, namelist, dir):

  """ KMZ create from dir

  Args:
    zipfilename: .zip/.kmz file to create
    namelist: list of filenames to archive
    dir: directory of files

  """

  zfd = zipfile.ZipFile(zipfilename,
                        mode = 'w',
                        compression = zipfile.ZIP_DEFLATED)

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

