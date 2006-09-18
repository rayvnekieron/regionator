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

""" class RegionHandler

Base class to derive for callbacks from Regionator

Use with kml.regionator.Regionator().

"""

class RegionHandler:

  """ Each method called for Region

  Methods called in the following order per Region.

  1) Start()
  2) PixelLod()
  3) Data()
  4) End()
  5) Kml()

  """

  def Start(self,region):

    """ First visit to this region.

    Derived class implements this to query data for this region.
    This is called before recursing to children.

    Return value determines recursion depth.

    Returns:
      [False,False] No data in this region, recurse no further.
      [True,False] Have data in this region, but no children do.
      [True,True] Have data in this region, and children might.
    """
    return [False,False]

  def End(self,region):

    """ Sub-region post-recursion handling

    This is called after recursing on all children.
    """

  def Styles(self, region):

    """ <Style>'s, <StyleMap>'s, <styleUrl>
    """
    return None

  def Schemas(self, region):

    """ <Schema>'s
    """
    return None

  def Data(self,region):

    """ KML data for this region

    Derived class implements this to return data for this region.

    This default implementation returns no data for any region.

    Returns:
      KML fragment for KML data in this region
    """

    return ''

  def PixelLod(self,region):

    """ Request for pixel lod range for this region

    Default implementation returns (128,-1).

    Returns:
      (minLodPixels,maxLodPixels)
    """

    minPixels = 128
    maxPixels = -1 # accumulates down the hierarchy
    return (minPixels,maxPixels)

  def Kml(self,region,kmlfile,kml):

    """ Completed KML generated for this region

    The derived class is left to write out the
    completed KML for the region.

    Args:
      region: kml.region.Region
      kmlfile: NetworkLink/Link/href name to this region
      kml: KML string generated for this region

    Returns:
      Nothing
    """
