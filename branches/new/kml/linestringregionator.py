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

""" class LineStringRegionator

Rudimentary specialization of kml.featureregionator.FeatureRegionator
showing one technique for organizing LineString data.

1) create kml.linestringregionator.LineStringRegionator()
2) SetFade(minfade,maxfade)
3) Regionate()

"""

import kml.featureregionator

class LineStringRegionator(kml.featureregionator.FeatureRegionator):

  """
  Build Region hierarchy of existing KML LineStrings based on "size"

  DEPRECATED: Use kml.kmlregionator
  """

  def ExtractItems(self):
    doc = self.GetDoc()
    pms = doc.getElementsByTagName('Placemark')
    for pm in pms:
      ls = pm.getElementsByTagName('LineString')
      if not ls:
        continue
      coords = ls[0].getElementsByTagName('coordinates')
      (size,lonlat) = self.AddLinestringCoordinates(coords[0])
      if lonlat.__len__() > 0:
        witem = (size,lonlat, pm.toxml())
        self.AddWeightedItem(witem)

