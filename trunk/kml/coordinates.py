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
