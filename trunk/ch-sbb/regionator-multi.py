#!/usr/bin/python

# Build a RbNL of stations icons with visual details of connections
# revealed when a station icon is highlighted.

import os
import kml.csvregionator
import kml.dashboard
import kml.featureset
import kml.genkml
import kml.genxml

station_point_csv='ch-stations.csv'
station_connections_csv='ch-connections.csv'
styleurl='../style/poly.kml#station_icon'
rootkml='ch-multi-root.kml'
dir='ch-multi-dir'

# Same as scripts/csvregionator.py:
minlod = 256
maxper = 16

def CreateConnectionLines(lon, lat, connection_list):
  """
  Args:
    connection_list: list of (lon, lat)
  Returns:
    linestring_kml_list: list of '<LineString>...</LineString>'
  """
  linestring_kml_list = []
  for (conn_lon, conn_lat) in connection_list:
    linestring_kml = kml.genkml.SimpleLineString(lon, lat, conn_lon, conn_lat)
    linestring_kml_list.append(linestring_kml)
  return linestring_kml_list

def CreatePlacemark(lon, lat, name, description, connection_list, style_url):
  """Create a MultiGeometry Placemark
  Args:
    lon, lat: location
    name: station name (unicode)
    connection_list: list of tuples: (station_name, connection_count)
    style_url: url#id to kml file with Style of id=id
  Returns:
    kml: '<Placemark>...<MultiGeometry>..</MultiGeometry</Placemark>'
  """
  multigeometry = kml.genxml.MultiGeometry()
  multigeometry.AddGeometry(kml.genkml.Point(lon,lat))
  for linestring_kml in CreateConnectionLines(lon, lat, connection_list):
    multigeometry.AddGeometry(linestring_kml)
  placemark = kml.genxml.Placemark()
  placemark.name = name
  placemark.description = description
  placemark.styleUrl = style_url
  placemark.Set_Geometry(multigeometry.xml())
  return placemark.xml()
  

# Parse the stations CSV to create a map of name to station info.
stations = {}
f = open(station_point_csv, 'r')
for csv_line in f:
  (score, lon, lat, name, description, style_url) = \
        kml.csvregionator.ParseCsvLine(csv_line, 'utf-8')
  stations[name] = (score, lon, lat, name, description)

# Parse the connections CSV to create a map of name to a list of connections.
connections = {}
def AddConnection(from_station, to_station):
  if connections.has_key(from_station):
    connections[from_station].append(to_station)
  else:
    connections[from_station] = [to_station]

f = open(station_connections_csv, 'r')
for csv_line in f:
  tuple = csv_line.split('|')
  if len(tuple) > 2:
    from_station = tuple[0].decode('utf-8')
    to_station = tuple[1].decode('utf-8')
    AddConnection(from_station, to_station)
    AddConnection(to_station, from_station)


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
  placemark_kml = CreatePlacemark(lon, lat, name, description,
                                  connection_list, styleurl)
  feature_set.AddWeightedFeatureAtLocation(score, lon, lat, placemark_kml)

# Sort the FeatureSet and regionate.
feature_set.Sort()
os.makedirs(dir)
rtor = kml.featureset.Regionate(feature_set, minlod, maxper, rootkml, dir, True)

# Create the Region "dashboard"
kml.dashboard.MakeDashBoard(rtor, 'db.kml')

