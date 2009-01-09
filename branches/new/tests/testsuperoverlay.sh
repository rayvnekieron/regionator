#!/bin/sh

# superoverlay.py requires gdal and gdal python bindings...

# http://landsat.gsfc.nasa.gov/data/Browse/Features/NASA_KSC.jpg

ksc=NASA_KSC.jpg

./testextractor.py

# will properly fail due to no bbox info in a .jpg
superoverlay.py $ksc x x

# use GroundOverlay LatLonBox
kmlsuperoverlay.py -i $ksc -k ksc-llb-0.kml -r llb-0.kml -d llb-0

# use GroundOverlay LatLonBox + drawOrder
kmlsuperoverlay.py -i $ksc -k ksc-llb-d.kml -r llb-d.kml -d llb-d

# use GroundOverlay LatLonBox + altitude
kmlsuperoverlay.py -i $ksc -k ksc-llb-a.kml -r llb-a.kml -d llb-a

# use GroundOverlay LatLonBox + TimeSpan
kmlsuperoverlay.py -i $ksc -k ksc-llb-t.kml -r llb-t.kml -d llb-t

# LatLonBox plus the full trifecta: drawOrder, altitude, TimeSpan
kmlsuperoverlay.py -i $ksc -k ksc-llb-3.kml -r llb-3.kml -d llb-3

# same as above with old mainline
superoverlay.py $ksc ksc-llb-3.kml llb-3-old.kml llb-3-old

diff -r llb-3 llb-3-old
