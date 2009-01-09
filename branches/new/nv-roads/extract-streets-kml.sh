#!/bin/sh
./cleanup.sh
unzip north-vancouver-streets.zip
ogr2ogr -f KML -s_srs "EPSG:26910" -t_srs "EPSG:4326" streets.kml streets.shp
