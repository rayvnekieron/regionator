#!/usr/bin/env python

# Build a RbNL of stations icons with visual details of connections
# revealed when a station icon is highlighted.

import os
import kml.csvregionator
import kml.dashboard
import kml.featureset
import kml.genkml
import kml.genxml
import chsbb

station_point_csv='ch-stations.csv'
station_connections_csv='ch-connections.csv'
styleurl='../style/poly.kml#station_icon'
rootkml='ch-multi-root.kml'
dir='ch-multi-dir'

# Same as scripts/csvregionator.py:
minlod = 256
maxper = 16

# Parse the stations CSV to create a map of name to station info.
stations = chsbb.ParseStationInfoCsv(station_point_csv)

# Parse the connections CSV to create a map of name to a list of connections.
connections = chsbb.ParseConnections(station_connections_csv)

# Get the list of (lon,lat) tuples of connections from this station.
def GetLocations(station_name):
  if not connections.has_key(station_name):
    return []
  locs = []
  for connecting_station_name in connections[station_name]:
    if stations.has_key(connecting_station_name):
      lon = stations[connecting_station_name][1]
      lat = stations[connecting_station_name][2]
      locs.append((lon,lat))
  return locs


# Create MultiGeometry Placemark for each station and add it
# to the FeatureSet.
feature_set = kml.featureset.FeatureSet()
for name in stations.keys():  # XXX proper iterator
  (score, lon, lat, name, description) = stations[name]
  connection_list = GetLocations(name)
  placemark_kml = chsbb.CreateMultiPlacemark(lon, lat, name, description,
                                             connection_list, styleurl)
  feature_set.AddWeightedFeatureAtLocation(score, lon, lat, placemark_kml)

# Sort the FeatureSet and regionate.
feature_set.Sort()
os.makedirs(dir)
rtor = kml.featureset.Regionate(feature_set, minlod, maxper, rootkml, dir, True)

# Create the Region "dashboard"
kml.dashboard.MakeDashBoard(rtor, 'db.kml')

