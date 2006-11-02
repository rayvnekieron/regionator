#!/bin/sh

# superoverlay.py requires gdal and gdal python bindings...

# http://landsat.gsfc.nasa.gov/data/Browse/Features/NASA_KSC.jpg

ksc=NASA_KSC.jpg

./testextractor.py $ksc

# will properly fail due to no bbox info in a .jpg
superoverlay.py $ksc x x

# use GroundOverlay LatLonBox
superoverlay.py $ksc ksc-llb-0.kml llb-0.kml llb-0

# use GroundOverlay LatLonBox + drawOrder
superoverlay.py $ksc ksc-llb-d.kml llb-d.kml llb-d

# use GroundOverlay LatLonBox + altitude
superoverlay.py $ksc ksc-llb-a.kml llb-a.kml llb-a

# use GroundOverlay LatLonBox + TimeSpan
superoverlay.py $ksc ksc-llb-t.kml llb-t.kml llb-t

# LatLonBox plus the full trifecta: drawOrder, altitude, TimeSpan
superoverlay.py $ksc ksc-llb-3.kml llb-3.kml llb-3
