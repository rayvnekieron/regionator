#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chsbb
import kml.genkml
import kml.genxml

zurich = 'Zürich HB'
station_list = [('Zug','ffff0000'),
                ('Luzern','ff0000ff'),
                (zurich,'ff00ffff')]
outfile = 'ch-connections.kml'

station_point_csv = 'ch-stations.csv'
station_connections_csv = 'ch-connections.csv'

stations = chsbb.ParseStationInfoCsv(station_point_csv)
connections = chsbb.ParseConnections(station_connections_csv)

def CreateStyleLineStyle(id, color):
  linestyle = kml.genxml.LineStyle()
  linestyle.color = color
  style = kml.genxml.Style()
  style.id = id
  style.LineStyle = linestyle.xml()
  return style.xml()


def CreateConnectionPlacemarks(station_name, styleurl):
  if not stations.has_key(station_name):
    return None
  lon = stations[station_name][1]
  lat = stations[station_name][2]
  placemark_kml = []
  for connecting_station_name in connections[station_name]:
    if stations.has_key(connecting_station_name):
      to_lon = stations[connecting_station_name][1]
      to_lat = stations[connecting_station_name][2]
      placemark = kml.genxml.Placemark()
      placemark.name = 'to %s' % connecting_station_name
      placemark.Geometry = kml.genkml.SimpleLineString(lon, lat, to_lon, to_lat)
      placemark.styleUrl = styleurl
      placemark_kml.append(placemark.xml())

  return placemark_kml

def CreateConnectionsFolder(station_name, styleurl):
  folder = kml.genxml.Folder()
  folder.name = 'Connections from %s' % station_name
  folder.open = '0'
  for placemark_kml in CreateConnectionPlacemarks(station_name, styleurl):
    folder.Add_Feature(placemark_kml)
  return folder.xml()

k = kml.genxml.Kml()
doc = kml.genxml.Document()
for (name_utf, color) in station_list:
  name = name_utf.decode('utf-8')
  style_id = 'style_%s' % name
  doc.Add_Style(CreateStyleLineStyle(style_id, color))
  style_url = '#%s' % style_id
  doc.Add_Feature(CreateConnectionsFolder(name, style_url))
k.Feature = doc.xml()

f = open(outfile, 'w')
f.write(k.xml().encode('utf-8'))
f.close()

