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


import sys
import os

import kml.image
import kml.superoverlayinfo
import kml.superoverlaykml
import kml.superoverlaytiles
import kml.tile
import kml.version

def SuperOverlay(imagefile, root, dir, n=None, s=None, e=None, w=None):

  """This creates a SuperOverlay.

  This creates a Region-based NetworkLink hierarchy of KML GroundOverlays
  from the given image at the specified location.  The image file is
  not altered.

  If the input image is a north-up EPSG:4326 (WGS 84) geotiff
  the image bounding box (north, south, east, west edges) is
  taken from the geotiff tags.  If bounding box arguments are
  supplied the geotiff tags are not used.

  If the input image is not a geotiff the image bounding box
  must be supplied.

  The specified output directory must not already exist.
  All links between KML and image tiles within this directory
  are relative such that the directory can be used either
  locally or copied to the appropriate http-serving directory
  for access via a http-based NetworkLink root file.

  The root file is a small NetworkLink KML file which points
  to the top of the SuperOverlay.  The href to 1.kml should be
  changed to be the URL of the directory.  This file is
  distributed to users of the SuperOverlay.  Note that the
  NetworkLink within is a Region-based load and that opening
  this file in Google Earth neither loads any imagery nor
  flies to the SuperOverlay.  When the user flies to the
  vicinity of the SuperOverlay this first NetworkLink is loaded
  which triggers further NetworkLink loads within the SuperOverlay
  as appropriate for the users viewpoint.

  A KML file of one LineString box per image tile in the
  created image hierachy is saved to dir/qidboxes.kml.  This is
  created for debugging and illustration purposes and is not
  required for proper functioning of the SuperOverlay.
  Note that a LineString does not exactly follow a longitude line.

  Error handling is not graceful: partial output data is not removed.
  and error messages may come in the form of a Python exception dump.

  Args:
    imagefile: image file
    root: where to store root KML
    dir: where to store KML hierarchy and image tiles
    n,s,e,w: edges of image, not required if img is geotiff

  Returns:
    bool: True on complete success, False on any failure
  """

  print 'version',kml.version.Revision()
  
  os.makedirs(dir)
  
  image = kml.image.Image(imagefile)
  if n and s and e and w:
    image.SetNSEW(n,s,e,w)
  
  if not image.ValidNSEW():
    (n,s,e,w) = image.NSEW()
    print 'image bounds not valid: n=%f,s=%f,e=%f,w=%f' % (n,s,e,w)
    return False
  
  print 'original dimensions',image.Dimensions()
  
  fmt = image.OutputFormat()
  twid = 512
  tht = 512
  
  # Phase 1 - find the regions with tiles
  
  superoverlayinfo = kml.superoverlayinfo.SuperOverlayInfo(image,twid,tht)
  rtor = superoverlayinfo.Regionate()
  maxdepth = rtor.MaxDepth()
  print 'maxdepth',maxdepth
  print 'count',rtor.RegionCount()
  rootregion = superoverlayinfo.RootRegion()
  print 'root region',rootregion.NSEW()
  tiles = superoverlayinfo.Tiles()
  
  # Phase 2 - generate the KML
  
  base_draworder = 1
  superoverlaykml = kml.superoverlaykml.SuperOverlayKML(rootregion,tiles,maxdepth,fmt,base_draworder,dir)
  superoverlaykml.Regionate()
  
  # debug linestring boxes
  
  qidboxes = os.path.join(dir, 'qidboxes.kml')
  kml.qidboxes.MakeQidBoxes(rtor, qidboxes)
  
  # Phase 3 - chop out image tiles
  
  superoverlaytiles = kml.superoverlaytiles.SuperOverlayTiles(rootregion,tiles,imagefile,dir,fmt,256,256)
  superoverlaytiles.Regionate()
  
  kml.regionator.MakeRootKML(root,rootregion,128,dir)
 
  return True
