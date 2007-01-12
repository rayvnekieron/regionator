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

""" class PlacemarkRegionator

A specialization of FeatureRegionator for Placemarks.

Derives from FeatureRegionator and implements ExtractItems.

"""

import kml.featureregionator

# AbstractRegionator does:
# 1) saves KML parse to self._doc
# 2) calls out to extractitems for specialization to create self._items
# 3) calls regionator to create KML Region NetworkLink hierarchy

class PlacemarkRegionator(kml.featureregionator.FeatureRegionator):

  """

  Find all Placemark/Point/coordinates in the parsed KML document.

  """
 

  def ExtractItems(self):
    doc = self.GetDoc()
    placemarks = doc.getElementsByTagName('Placemark')
    if self.GetVerbose():
      print 'extracting %d placemarks...' % placemarks.__len__()
    for placemark in placemarks:
      point = placemark.getElementsByTagName('Point')
      if not point:
        return
      coords = point[0].getElementsByTagName('coordinates')
      lonlat = self.AddPointCoordinates(coords[0])
      if lonlat.__len__() > 0:
        item = (lonlat, placemark.toxml())
        self.AddItem(item)


