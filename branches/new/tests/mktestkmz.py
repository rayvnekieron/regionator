#!/usr/bin/env python

import zipfile
import os.path

kml = [ 'test.kml',
        'usboxes',
        'ancestors.kml',
        'pm2root.kml',
        'pm2',
        'ls2root.kml',
        'ls2',
        'gridso.kml',
        'folder-regions.kml',
        'terra.kml',
        'terra_w.jpg',
        'terra_e.jpg',
        'llb-0',
        'llb-0.kml',
        'llb-d',
        'llb-d.kml',
        'llb-t',
        'llb-t.kml',
        'llb-a',
        'llb-a.kml',
        'llb-3'
        'llb-3.kml']

zfd = zipfile.ZipFile('test.kmz', mode='w', compression=zipfile.ZIP_DEFLATED)

for item in kml:
  if os.path.isdir(item):
    for file in os.listdir(item):
      zpath = os.path.join(item,file)
      zfd.write(zpath)
  if os.path.isfile(item):
    zfd.write(item)

zfd.close()
