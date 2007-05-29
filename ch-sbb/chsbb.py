
import kml.csvregionator
import kml.genkml
import kml.genxml

def ParseStationInfoCsv(csvfile):
  """ Parse the stations CSV to create a map of name to station info.
  Args:
    csvfile:
  Returns:
    map: station name to (score, lon, lat, name, description, style_url)
  """
  station_info = {}
  f = open(csvfile, 'r')
  for csv_line in f:
    (score, lon, lat, name, description, style_url) = \
      kml.csvregionator.ParseCsvLine(csv_line, 'utf-8')
    station_info[name] = (score, lon, lat, name, description)
  return station_info


def AddConnection(connections, from_station, to_station):
  if connections.has_key(from_station):
    connections[from_station].append(to_station)
  else:
    connections[from_station] = [to_station]

def ParseConnections(csvfile):
  # Parse the connections CSV to create a map of name to a list of connections.
  connections = {}
  f = open(csvfile, 'r')
  for csv_line in f:
    tuple = csv_line.split('|')
    if len(tuple) > 2:
      from_station = tuple[0].decode('utf-8')
      to_station = tuple[1].decode('utf-8')
      AddConnection(connections, from_station, to_station)
      AddConnection(connections, to_station, from_station)
  return connections


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

def CreateMultiPlacemark(lon, lat, name, description,
                         connection_list, style_url):
  """Create a MultiGeometry Placemark
  Args:
    lon, lat: location
    name: station name (unicode)
    connection_list: list of tuples: (station_name, connection_count)
    style_url: url#id to kml file with Style of id=id
  Returns:
    kml: '<Placemark>...<MultiGeometry>..</MultiGeometry></Placemark>'
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

