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

def ParsePointCoordinates(coordinates):

  """ Parse <coordinates> for a Point

  Permits a sloppy Point coordinates.

  Arg:
    coordinates: lon,lat,alt or lon,lat with spaces allowed

  Returns:
    None: if coordinates was not 2 or 3 comma separated numbers
    (lon,lat): float tuple
    (lon,lat,alt): float tuple
  """
  p = coordinates.split(',')
  if len(p) == 2:
    return (float(p[0].strip()), float(p[1].strip()))
  elif len(p) == 3:
    return (float(p[0].strip()), float(p[1].strip()), float(p[2].strip()))
  return None
 

def ParseCoordinates(coordinates):

  """ Parse <coordinates> contents

  Args:
    coordinates: character data of <coordinates> element

  Returns:
    list of float tuples: (lon,lat) or (lon,lat,alt)
  """

  # See if it's a sloppy Point
  point = ParsePointCoordinates(coordinates)
  if point:
    return [point]
  points = []
  clist = coordinates.split() # split on whitespace
  for coord in clist:
    point = coord.split(',')
    if len(point) == 3:
        lon = float(point[0].strip())
        lat = float(point[1].strip())
        alt = float(point[2].strip())
        points.append((lon,lat,alt))
    elif len(point) == 2:
        lon = float(point[0].strip())
        lat = float(point[1].strip())
        points.append((lon,lat))
  return points


class Coord3d(object):
  """
  A simple class to represent a single lng, lat, alt coordinate string.

  The class must be initialized with one of a string, tuple or list
  representing either two or three coordinates. If a string, the coordinates
  must be delimited by commas.
  """
  
  def __init__(self, coords=None):
    """Initializes a Coord3d to 0,0,0 (default) or to value of coords arg.
    """
    self.__lon = 0.0
    self.__lat = 0.0
    self.__alt = 0.0
    if coords is not None:
      if isinstance('', coords.__class__):
        self.from_string(coords)
      elif isinstance(u'', coords.__class__):
        self.from_string(coords) # XXX need to do something special w/ unicode?
      elif isinstance((), coords.__class__):
        self.from_tuple(coords)
      elif isinstance([], coords.__class__):
        self.from_list(coords)
      else: # didn't understand type, set defaults anyway
        self.from_tuple(0,0,0)
    
  def from_string(self, s):
    coords = s.split(',')
    self.from_list(coords)

  def from_tuple(self, t):
    coords = list(t)
    self.from_list(coords)

  def from_list(self, l):
    assert 2 <= len(l) <= 3
    self.__lon = float(l[0])
    self.__lat = float(l[1])
    if len(l) == 3:
      self.__alt = float(l[2])
    else:
      self.__alt = 0.0

  def Set_lon(self, lon):
    self.__lon = float(lon)
  
  def Get_lon(self):
    return self.__lon
  
  def Set_lat(self, lat):
    self.__lat = float(lat)
  
  def Get_lat(self):
    return self.__lat
  
  def Set_alt(self, alt):
    self.__alt = float(alt)
  
  def Get_alt(self):
    return self.__alt
  
  lon = property(fget=Get_lon, fset=Set_lon)
  lat = property(fget=Get_lat, fset=Set_lat)
  alt = property(fget=Get_alt, fset=Set_alt)
  
  def to_string(self):
    s = '%0.6f,%0.6f,%0.6f' % (self.__lon, self.__lat, self.__alt)
    return s


class Coord3dArray(object):
  """A simple class to represent multiple coordinate strings.
  """

  def __init__(self, coords=None):
    self.__coord3d_array = []
    if coords is not None:
      self.Set_coord3d_array(coords)

  def Set_coord3d_array(self, coords):
    if isinstance('', coords.__class__):
      self.from_string(coords)
    elif isinstance(u'', coords.__class__):
      self.from_string(coords) # XXX need to do something special w/ unicode?
    elif isinstance((), coords.__class__):
      self.from_tuple(coords)
    elif isinstance([], coords.__class__):
      self.from_list(coords)
    else: # didn't understand type, set defaults anyway
      pass

  def Get_coord3d_array(self):
    return self.__coord3d_array

  coords = property(fget=Get_coord3d_array, fset=Set_coord3d_array)

  def from_string(self, coord_str):
    # Coordinate strings may be separated by new lines, tabs or spaces?
    coord_str.replace('\n', ' ') # scrap the new lines
    coord_str.replace('\t', ' ') # and the tabs
    while coord_str.find('  ') != -1: # and any  multiple spaces
      coord_str = coord_str.replace('  ', ' ')
    foo = 0
    if coord_str.find(' ,') != -1: foo = 1
    coord_str = coord_str.replace(', ', ',') # space to right of comma
    coord_str = coord_str.replace(' ,', ',') # space to left of comma
    coord_list = coord_str.split(' ')
    self.from_list(coord_list)

  def from_tuple(self, t):
    l = list(t)
    self.from_list(l)

  def from_list(self, l):
    for coord_str in l:
      self.__coord3d_array.append(Coord3d(coord_str))

  def Get_length(self):
    return len(self.__coord3d_array)
  
  def to_string(self):
    ret = []
    for coord3d in self.__coord3d_array:
      ret.append(coord3d.to_string())
    return ' '.join(ret)

  length = property(fget=Get_length)

  def first_equals_last(self):
    """Return true iff first and last coordinates in array are equal
    """
    # XXX implement fuzzy equals for precision errors?
    first = self.__coord3d_array[0]
    last = self.__coord3d_array[len(self.__coord3d_array)-1]
    if (first.lon == last.lon) and \
       (first.lat == last.lat) and \
       (first.alt == last.alt):
      return True
    else:
      return False

  def close_loop(self):
    """Appends first coordinate in array to array if first != last
    """
    if self.first_equals_last(): return
    self.__coord3d_array.append(self.__coord3d_array[0])

  def is_clockwise(self):
    """Test a coordinate array for a negative rotation (clockwise winding
    order).
    Returns:
      - True if rotation is negative
      - False if rotation is positive
      - None if no coordinates set
    """
    if not self.__coord3d_array: return None
    verts = self.__coord3d_array
    num_pts = len(verts)
    if num_pts < 3: return True # XXX ambiguous
    sum = 0.0
    for i in range(num_pts - 1):
      sum += verts[i].lon * verts[i+1].lat - \
             verts[i].lat * verts[i+1].lon
    sum += verts[num_pts-1].lon * verts[0].lat - \
           verts[num_pts-1].lat * verts[0].lon
    if sum < 0.0: return True
    else: return False

  def reverse_winding_order(self):
    """Reverses the rotation of a coordinate array.
    """
    if not self.__coord3d_array: return
    verts = self.__coord3d_array
    for i in range(len(verts) / 2):
      tmp_vert = verts[i]
      pos = len(verts) - i - 1
      verts[i] = verts[pos]
      verts[pos] = tmp_vert
    self.__coord3d_array = verts


