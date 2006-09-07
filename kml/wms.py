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

WMS utilities

"""

import kml.region
import kml.genkml


def AppendWMSBBOX(href,n,s,e,w):

  """ Creates a WMS format BBOX.

  WMS BBOX: minX,minY,maxX,maxY or w,s,e,n in WGS84

  Args:
    href: base url
    n,s,e,w: bounding box in decimal degress

  Returns:
    href + BBOX=w,s,e,n

  """

  bbox='BBOX=%f,%f,%f,%f' % (w,s,e,n)
  return href + bbox


def WMSGroundOverlay(wmsurl, region, draworder):

  """ Create a GroundOverlay for a WMS image

  Args:
    wmsurl: base wms url (no w/o BBOX)
    draworder: GroundOverlay drawOrder
    region: kml.region.Region for image BBOX and GO LatLonBox

  Returns:
    KML: <GroundOverlay>...</GroundOverlay>
  """

  (n,s,e,w) = region.NSEW()
  href = AppendWMSBBOX(wmsurl,n,s,e,w)
  return kml.genkml.GroundOverlay(n,s,e,w,href,draworder)

