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

"""class Tile

A Tile is part of an Image.

"""

import kml.region

class Tile:

  """class Tile

  Created by kml.image.Tile.

  """

  def __init__(self,x,y,wid,ht,n,s,e,w):
    self.__x = x
    self.__y = y
    self.__wid = wid
    self.__ht = ht

    self.__n = n
    self.__s = s
    self.__e = e
    self.__w = w

  def Wid(self):
    return self.__wid

  def Ht(self):
    return self.__ht

  def Info(self):

    """Extraction info in pixels

    Returns:
      (xoffset,yoffset,width,height)
    """

    return (self.__x,self.__y,self.__wid,self.__ht)

  def NSEW(self):

    """Bounding box

    Returns the geographic extent of the tile.

    Returns:
      (north,south,east,west)
    """

    return (self.__n,self.__s,self.__e,self.__w)


def WriteTileFile(tilefile,tilelist):

  """ Saves a list of kml.tile.Tile's to an ascii file

  Args:
    tilefile - the file to write to (must not already exist)
    tilelist - dictionator of kml.tile.Tile's indexed qid
  """

  f = open(tilefile,'w')
  for qid in tilelist.keys():
    (x,y,wid,ht) = tile.Info()
    (n,s,e,w) = tile.NSEW()
    str = '%s %f %f %f %f %f %f %f %f\n' % (qid,x,y,wid,ht,n,s,e,w)
    f.write(str)
  f.close()


class TileSet:

  """ Reads what WriteTileFile writes

  Args:
    tilefile - ascii file of image tiles

  """

  def __init__(self,tilefile):

    self.__maxdepth = 0
    self.__tiles = {}

    f = open(tilefile,'r')
    for line in f:
      ls = line.strip().split(' ')
      qid = ls[0]
      x = float(ls[1])
      y = float(ls[2])
      wid = float(ls[3])
      ht = float(ls[4])
      n = float(ls[5])
      s = float(ls[6])
      e = float(ls[7])
      w = float(ls[8])

      tile = Tile(x,y,wid,ht,n,s,e,w)
  
      self.__tiles[qid] = tile

      if len(qid) > self.__maxdepth:
        self.__maxdepth = len(qid)

      if qid == '0':
        self.__root = kml.region.Region(n,s,e,w,'0')


  def Tiles(self):

    return self.__tiles


  def MaxDepth(self):

    return self.__maxdepth


  def RootRegion(self):

    return self.__root
 

 
