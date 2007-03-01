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

""" class Region

A Region manages <Region> bounding box and children

"""

class Region:

  """
  A Region is created with a given bounding box and node id.

  Use Child() to create sub-regions.

  """

  def __init__(self,n,s,e,w,qid):

    """ Create a Region at the given location and node id.

    Args:
      n,s,e,w: float
      qid: string
    """

    self.__n = n
    self.__s = s
    self.__e = e
    self.__w = w
    self.__qid = qid
    self.__id = None
    self.__x = (e+w)/2. # XXX
    self.__y = (n+s)/2. # XXX

  def SetId(self,id):
    self.__id = id

  def Id(self):
    return self.__id

  def NSEW(self):

    """ Return bounding box as float tuple

    Returns:
      (n,s,e,w): floats
    """

    return (self.__n,self.__s,self.__e,self.__w)

  def NSEWstring(self):

    """ Return bounding box as string tuple

    Returns:
      (n,s,e,w): strings
    """

    return (repr(self.__n),repr(self.__s),repr(self.__e),repr(self.__w))

  def ResetQid(self,qid):
    self.__qid = qid

  def Qid(self):
    return self.__qid

  def Depth(self):
    return self.__qid.__len__()

  def MidPoint(self):
    return (self.__x,self.__y)

  def Child(self,child):

    """ Return the given sub-region

    This method provides the meaning of a "qid"

    NW NE  0 1  00 01
    SW SE  2 3  10 11

    0 bit is x offset, 1 bit is y offset (upper-left origin).

    Args:
      child: '0','1','2', or '3'

    Returns:
      Region
    """

    if child == '0':
      return Region(self.__n,self.__y,self.__x,self.__w,self.__qid+'0')
    if child == '1':
      return Region(self.__n,self.__y,self.__e,self.__x,self.__qid+'1')
    if child == '2':
      return Region(self.__y,self.__s,self.__x,self.__w,self.__qid+'2')
    if child == '3':
      return Region(self.__y,self.__s,self.__e,self.__x,self.__qid+'3')
    # XXX
    print 'Region.Child() something is badly broken'

  def _Region(self,qid):
    r = self.Child(qid[0])
    if qid.__len__() == 1:
      return r
    return r._Region(qid[1:])

  def Region(self,qid):

    """ Return the region for the given node in the hiearchy.

    Returns:
      kml.region.Region
    """

    if qid[0] != '0':
      return 0
    if qid == '0':
      return self
    return self._Region(qid[1:])

  def InRegion(self,lon,lat):

    """ Is this this point in this Region?

    Args:
      lon,lat: the point

    Returns:
      Boolean
    """

    if lat <= self.__n and lat >= self.__s and lon <= self.__e and lon >= self.__w:
      return True
    return False

  def Contains(self,r):

    """ Is Region r wholly within this Region?

    Args:
      r: kml.region.Region

    Returns:
      Boolean

    """

    (n,s,e,w) = r.NSEW()
    if n <= self.__n and s >= self.__s and e <= self.__e and w >= self.__w:
      return True
    return False

  def WhichChildForPoint(self, lon, lat):
    for q in ['0','1','2','3']:
      c = self.Child(q)
      if c.InRegion(lon, lat):
        return c
    return None

  # return which child node contains r
  # return 0 if none
  def _WhichChild(self,r):
    for q in ['0','1','2','3']:
      c = self.Child(q)
      if c.Contains(r):
        return c
    return 0

  def _Search(self,r):
    child = self._WhichChild(r)
    if child:
      return child._Search(r)

    # Was not in any of the child regions so
    # the search is complete with us
    return self


  def Snap(self,n,s,e,w):

    """
    Find the lowest level region enclosing the given Region
    """ 

    r = Region(n,s,e,w,'0')
    return self._Search(r)


  def SnapPoint(self, lon, lat, maxdepth):
    for q in ['0','1','2','3']:
      c = self.Child(q)
      if c.InRegion(lon, lat):
        if maxdepth > 2:
          return c.SnapPoint(lon, lat, maxdepth - 1)
        return c
    # watch that indent...
    return None


  def Grid(self):
    return Grid(self.__qid)


  def ParentQid(self):
    if self.__qid == '0':
      return '0'
    return self.__qid[0:self.Depth()-1]



def RootRegion():
  # yes n=180,s=-180
  return Region(180.,-180.,180.,-180.,'0')


def RootSnap(n,s,e,w):
  root = RootRegion()
  r = root.Snap(n,s,e,w)
  r.ResetQid('0')
  return r

def RootSnapPoint(lon, lat, maxdepth):
  root = RootRegion()
  r = root.SnapPoint(lon, lat, maxdepth)
  r.ResetQid('0')
  return r

def Breadth(depth):

  """ Complexity at this depth.

  Depth 1 == Breadth 1
  Depth 2 == Breadth 2
  Depth 3 == Breadth 4
  Depth n == Breadth 2 ^ (n-1)

  Args:
    depth: hierarchy depth

  Returns:
    Number of sub-regions across at this depth.
  """

  return 2 ** (depth-1)

def Location(child):

  """ Return x,y offset of Region

  See comment in Region.Child()

  Args:
    child: '0','1','2','3'

  Returns:
    (x,y): lower-left origin
  """

  childnum = int(child)

  x = childnum & 1 # mask the y bit
  y = childnum >> 1 # shift over the y bit

  y = not y

  return (x,y)


def _Grid(qid):
  depth = len(qid)
  (x,y) = Location(qid[0])
  if depth == 1:
    return (x,y)

  # Recurse to children
  (cx,cy) = _Grid(qid[1:])
  # Scale this level add in child offset
  x = Breadth(depth) * x + cx
  y = Breadth(depth) * y + cy

  return (x,y)

def Grid(qid):

  """
  Relative location of the specified node.

  Args:
    qid: node

  Returns:
    (x,y):
  """
  if qid == '0':
    return (0,0)
  return _Grid(qid[1:]) # qid[0] always '0'

def DepthScale(d,max):
  return Breadth(max - d + 1) * 8

# as depth increases color goes from b->r
def DepthColor(depth,maxdepth):
  r = (depth * 255)/maxdepth
  b = 255 - r
  g = 0
  return (b,g,r)

