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

"""class Image"""

import gdal

import kml.latlon
import kml.tile

class Image:

  """

  An Image holds basic information about an image file including geo-location.
  If the image file is a geotiff the geo-location info is extracted,
  otherwise the bounding box must be supplied.  The image is required to
  be "north-up" and otherwise latitude and longitude aligned.

  This class is read-only w.r.t. to the image file.

  1) kml.image.Image(imgfile)
  2) kml.image.SetNSEW(n,s,e,w) - set bbox if imgfile not geotiff

  """

  def __init__(self,imgfile):
    self.__llb = kml.latlon.LatLonBox(0,0,0,0)
    self.SetFile(imgfile)

  def _ComputePixelsPerDegree(self):
    (n,s,e,w) = self.__llb.NSEW()
    self.__x_pixels_per_degree = self.__wid/(e - w)
    self.__y_pixels_per_degree = self.__ht/(n - s)

  def SetFile(self,imgfile):

    """Initialize the class based on the specified file

    If the image file is a geotiff it is expected to have
    proper (ESPG:4326) lat/lon bbox info.

    """

    self.__imgfile = imgfile
    ds = self.__ds = gdal.Open(imgfile)
    self.__wid = ds.RasterXSize
    self.__ht = ds.RasterYSize
    self.__gt = ds.GetGeoTransform()
    # Dont't crash if transform not north-up
    if self._ComputeLLBox():
      self._ComputePixelsPerDegree()

  def _ComputeLLBox(self):
    gt = self.__gt
    # gt[0],gt[3] == top,left
    if gt[2] and gt[4]:
      # print 'image not north up'
      return False
    if gt[5] > 0:
      # print 'funny xform'
      return False
    n = gt[3]
    s = gt[3] + gt[5] * self.__ht
    e = gt[0] + gt[1] * self.__wid
    w = gt[0]
    self.__llb.SetNSEW(n,s,e,w)
    return True

  def SetNSEW(self,n,s,e,w):

    """Set bbox

    Required if image file is not a gtiff or otherwise has no
    bounding box.

    Overrides gtiff bounding if such existed.

    """

    self.__llb.SetNSEW(n,s,e,w)
    self._ComputePixelsPerDegree()

  def NSEW(self):

    """Geo-location of image edges

    Returns:
      (north,south,east,west)
    """
    return self.__llb.NSEW()

  def ValidNSEW(self):

    """Is bounding box valid?

    Returns:
      Boolean:
    """

    return self.__llb.ValidNSEW()

  def HasPixels(self,n,s,e,w):

    """Does the image have any pixels in the given bounding box?

    Returns:
      True or False
    """
    (_n,_s,_e,_w) = self.__llb.NSEW()
    if _n > s and _s < n and _e > w and _w < e:
      return True
    return False


  def IsPartial(self,n,s,e,w):
    """Does the specified bbox extend beyond the image?

    Returns:
      True or False
    """
    (_n,_s,_e,_w) = self.__llb.NSEW()
    if w < _w or e > _e or n > _n or s < _s:
      return True
    return False

  def Fit(self,n,s,e,w):

    """ Shrink to fit...

    Adjusts the given bbox to enclose actual pixels

    Returns:
      (north,south,east,west)
    """
    (_n,_s,_e,_w) = self.__llb.NSEW()
    if w < _w:
      w = _w
    if e > _e:
      e = _e
    if n > _n:
      n = _n
    if s < _s:
      s = _s
    return (n,s,e,w)

  def Tile(self,n,s,e,w):

    """Returns a Tile at the specified geo-location

    A Tile holds the information required to extract
    the pixels for the given bbox.

    Returns:
      Tile
    """

    (_n,_s,_e,_w) = self.__llb.NSEW()
    (n,s,e,w) = self.Fit(n,s,e,w)

    x_degrees = w - _w
    x = self.__x_pixels_per_degree * x_degrees

    wid_degrees = e - w
    wid = self.__x_pixels_per_degree * wid_degrees

    y_degrees = _n - n
    y = self.__y_pixels_per_degree * y_degrees

    ht_degrees = n - s
    ht = self.__y_pixels_per_degree * ht_degrees
    
    tile = kml.tile.Tile(x,y,wid,ht,n,s,e,w)
    return tile

  def Dimensions(self):

    """Pixel dimensions of image

    Returns:
      (width,height)
    """

    return (self.__wid,self.__ht)

  def OutputFormat(self):

    """Best output format for this image

    Just a recommendation...

    If 1 or 3 channels: JPEG
    If 4 channels (assumed to be RGBA): PNG

    Returns:
        'PNG' or 'JPEG'
    """

    count = self.__ds.RasterCount
    if count == 4:
        return 'PNG'
    if count == 3 or count == 1:
        return 'JPEG'
    return ''

    
