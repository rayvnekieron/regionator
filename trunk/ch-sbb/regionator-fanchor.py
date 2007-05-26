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
rootkml='ch-featanchor-root.kml'
dir='ch-featanchor'

# Same as scripts/csvregionator.py:
minlod = 256
maxper = 16

# Do this now so we fail right away
os.makedirs(dir)

# Parse the stations CSV to create a map of name to station info
# and create a unique id for each station.
station_info = {}
f = open(station_point_csv, 'r')
count = 0
for csv_line in f:
  (score, lon, lat, name, description, style_url) = \
        kml.csvregionator.ParseCsvLine(csv_line, 'utf-8')
  id = 'st%d' % count
  count += 1
  station_info[name] = (score, lon, lat, name, description, id)

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
    if station_info.has_key(connecting_station_name):
      lon = station_info[connecting_station_name][1]
      lat = station_info[connecting_station_name][2]
      locs.append((lon,lat))
  return locs

# Create MultiGeometry Placemark for each station and add it
# to the FeatureSet.
feature_set = kml.featureset.FeatureSet()
for name in station_info.keys():  # XXX proper iterator
  (score, lon, lat, name, description, id) = station_info[name]
  feature_set.AddWeightedFeatureAtLocation(score, lon, lat, name)

name_to_qid = {}
qid_to_namelist = {}
# This finds the node for each name
class ChInfoRegionHandler(kml.featureset.FeatureSetRegionHandler):

  def __init__(self, fs, minpx, maxper):
    kml.featureset.FeatureSetRegionHandler.__init__(self, fs, minpx, maxper)

  def Start(self, region):
    start_ret = kml.featureset.FeatureSetRegionHandler.Start(self, region)
    if not start_ret[0]:
      # Nothing in this region
      return start_ret

    # Dig through the result to get a mapping from name to qid
    fs = self._node_feature_set[region.Qid()]
    namelist = []
    for (w,lon,lat,name) in fs:
      name_to_qid[name] = region.Qid()
      namelist.append(name)
    qid_to_namelist[region.Qid()] = namelist
    return start_ret

  def Data(self, region):
    # override FSRH.Data() because it expects the feature to be KML
    return None

def FindConnections(station_name):
  local_connections = []
  my_qid = name_to_qid[station_name]
  for connecting_station_name in connections[station_name]:
    if name_to_qid.has_key(connecting_station_name):
      qid = name_to_qid[connecting_station_name]
      if qid == my_qid:
        local_connections.append(connecting_station_name)
  return local_connections

def CreateBalloonFlyto(id, name):
  return '<a href="#%s|balloonFlyto">%s</a>' % (id, name)

def CreateDescriptionLinks(station_name):
  anchor_list = []
  local_connections = FindConnections(station_name)
  for name in local_connections:
    (score, lon, lat, name, description, id) = station_info[name]
    anchor_list.append(CreateBalloonFlyto(id, name))
  if anchor_list:
    return "<br/>\n".join(anchor_list)
  return None

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

def CreatePlacemark(id, lon, lat, name, connection_list, style_url):
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
  placemark.id = id
  placemark.name = name
  placemark.description = CreateDescriptionLinks(name)
  placemark.styleUrl = style_url
  placemark.Set_Geometry(multigeometry.xml())
  range = 1000
  tilt = 0
  heading = 0
  placemark.LookAt = kml.genkml.LookAt(lon, lat, range, tilt, heading)

  # placemark.LookAt = else lookat is for linestring spread...
  return placemark.xml()


class ChKmlRegionHandler(kml.regionhandler.RegionHandler):

  def Start(self, region):
    if qid_to_namelist.has_key(region.Qid()):
      return [True, True]
    return [False, False]

  def Data(self, region):
    placemarks = []
    for name in qid_to_namelist[region.Qid()]:
      connection_list = GetLocations(name)
      (score, lon, lat, name, description, id) = station_info[name]
      pm = CreatePlacemark(id, lon, lat, name, connection_list, styleurl)
      placemarks.append(pm)
    return "\n".join(placemarks)
    

def Regionate(kmldir):
  # Sort the FeatureSet and regionate.
  feature_set.Sort()
  ch_info_rhandler = ChInfoRegionHandler(feature_set, minlod, maxper)
  (n,s,e,w) = ch_info_rhandler.NSEW()
  rtor = kml.regionator.Regionator()
  rtor.SetRegionHandler(ch_info_rhandler)
  # rtor.SetVerbose(False)
  region = kml.region.RootSnap(n,s,e,w)
  rtor.Regionate(region)

  ch_kml_rhandler = ChKmlRegionHandler()
  rtor = kml.regionator.Regionator()
  rtor.SetRegionHandler(ch_kml_rhandler)
  rtor.SetOutputDir(kmldir)
  rtor.Regionate(region)
  return rtor

rtor = Regionate(dir)
if rtor:
  root_href = rtor.RootHref()
  region = rtor.RootRegion()
  kml.regionator.MakeRootForHref(rootkml, region, minlod, root_href)

