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

import os

def RootIconUrl(href, x, y, w, h):
  """Translate the old-style palette icon reference to its new-style URL
  Args:
    href: 'root://icons/palette-[2345].png'
    x,y,w,h: content of <x>,<y>,<w>,<h>
  Returns:
    url: 'http://maps.google.com/mapfiles/kml/pal4/icon54.png'
  """
  icon_number = (7 - y/h) * 8 + x/w
  (path,ext) = os.path.splitext(href)
  pal_number = int(path[-1:])
  return 'http://maps.google.com/mapfiles/kml/pal%d/icon%d.png' \
                                                   % (pal_number, icon_number)

def ListPalette(pal_num):
  """Return the URLs for all icons in the given palette
  Args:
    pal_num: [2345] 
  Returns:
    list: URL's http://maps.google.com/mapfiles/kml/palN/iconM.png
  """
  href = 'root://icons/palette-%d.png' % pal_num
  urls = []
  y = 224
  while y >= 0:
    x = 0
    while x < 256:
      urls.append(RootIconUrl(href, x, y, 32, 32))
      x += 32
    y -= 32
  return urls

def PrintAllRootIcons():
  """Print the URLs for all de-palettized old-style root://icons
  Prints top to bottom, left to right (in order of the icon number)
  """
  for pal_num in [2,3,4,5]:
    urls = ListPalette(pal_num)
    for url in urls:
      print url
