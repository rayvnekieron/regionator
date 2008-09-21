#!/usr/bin/env python

import kml.image

image = kml.image.Image('image.gif')
if image.OutputFormat() != 'GIF':
  print 'ERROR in kml.image.Image().OutputFormat'
