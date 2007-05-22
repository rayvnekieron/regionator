#!/bin/sh

# Same as regionator-basic.sh adding a styleUrl to each Placemark.
# See style/README for several styling possibilities.

global_style=../style/style.kml#station_icon
csvregionator.py ch-stations.csv ch-style-root.kml ch-style-dir $global_style
