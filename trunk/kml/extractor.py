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

""" class Extractor

Phase 3 of SuperOverlay creation.

Extract tiles from an image

Front-ends GDAL.  Input file and output driver must be
some format known to GDAL.

"""

import gdal
import tempfile
import os


class Extractor:

  """ class Extractor

  Create for Extractor the image file.
  Each tile is resampled to the specified size and written
  to a file of the given format.

  """

  def __init__(self,imgfile,twid,tht,fmt,verbose=False):

    """
    
    Args:
      imgfile: a gtiff
      twid,tht: extracted tile resample pixel width/height
      fmt: GDAL output driver name ('PNG','JPEG')
    """

    self.__in_ds = gdal.Open(imgfile)
    self.__twid = twid
    self.__tht = tht
    self.__fmt = fmt
    self.__verbose = verbose

    self.__bands = self.__in_ds.RasterCount

    print 'Extractor %s %d bands' % (imgfile,self.__bands)

    # Intermediate work must be in GTiff (?)
    self.__gtiff_driver = gdal.GetDriverByName('GTiff')

    # Output driver/format is whatever the user specifies
    # XXX handle bad/wrong fmt's less gracelessly
    self.__o_driver = gdal.GetDriverByName(fmt)

  def Extract(self,x,y,wid,ht,basename):

    """ Extract a tile into a file

    The given tile is extracted, resampled and saved
    according to the tile pixel dimensions and format
    specified at object __init__().
    
    Args:
      x,y: pixel offset
      wid,ht: pixel dimensions

    Returns:
      True: complete success
      False: any failure

    """

    # Get the tile's pixels resampled
    twid = self.__twid
    tht = self.__tht
    i_data = self.__in_ds.ReadRaster(x,y,wid,ht,buf_xsize=twid,buf_ysize=tht)

    # Have to Create out to GTiff first (?)
    (fd, tmpfile) = tempfile.mkstemp(suffix='GTiff')
    os.close(fd)
    o_ds = self.__gtiff_driver.Create(tmpfile,twid,tht,bands=self.__bands)
    o_ds.WriteRaster(0,0,twid,tht,i_data)

    # Save off using the specified driver
    filename = '%s.%s' % (basename,self.__fmt)
    self.__o_driver.CreateCopy(filename,o_ds)

    if self.__verbose:
      print filename

    # Delete the tmp file
    self.__gtiff_driver.Delete(tmpfile)

