#!/usr/bin/env python

# Life of a Feature
#
# A demonstration of KML elements and behavior common to all Features

import kml.genxml
import kml.genkml
import sys

loafkml = 'life-of-a-feature.kml'

def CreateStyle(id):

  balloonstyle = kml.genxml.BalloonStyle()
  text = []
  text.append('<b>$[name]</b>')
  text.append('$[description]')
  text.append('Longitude=$[lon], Latitude=$[lat]')
  text.append('<i>$[id]</i>')
  balloonstyle.text = '<![CDATA[%s]]>' % '<br/>'.join(text)
  balloonstyle.bgColor = 'ff82fff3' # light yellow

  itemicon = kml.genxml.ItemIcon()
  itemicon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'

  liststyle = kml.genxml.ListStyle()
  liststyle.listItemType = 'checkHideChildren'
  liststyle.bgColor = 'ffffb20b' # light blue
  liststyle.ItemIcon = itemicon.xml()

  style = kml.genxml.Style()
  style.id = id
  style.BalloonStyle = balloonstyle.xml()
  style.ListStyle = liststyle.xml()

  return style

def CreateExtendedData(nvp_list):
  extendeddata = kml.genxml.ExtendedData()
  for (name,value) in nvp_list:
    data = kml.genxml.Data()
    data.name = name
    data.value = value
    extendeddata.Add_Data(data.xml())
  return extendeddata

def CreateLonLat(lon, lat):
  ll = []
  ll.append(('lon', lon))
  ll.append(('lat', lat))
  return ll

def SetFeatureFields(id, feature, short, long, view, style_url, nvp_list):
  # Object-ness
  feature.id = id

  # Feature-ness
  feature.name = short
  feature.visibility = 0
  # feature.open
  # feature.atom_author
  # feature.atom_link
  # feature.address
  # feature.xal_AddressDetails
  # feature.phoneNumber
  feature.Snippet = long
  feature.description = long
  feature.AbstractView = view
  # feature.TimePrimitive
  feature.styleUrl = style_url
  # feature.StyleSelector
  # feature.Region
  if nvp_list:
    feature.Add_ExtendedData(CreateExtendedData(nvp_list).xml())

def CreateLOAF():
  style_id = 'shared-style'
  styurl = '#%s' % style_id

  style = CreateStyle(style_id)

  placemark = kml.genxml.Placemark()
  lon = 134.6
  lat = -20.47
  view = kml.genkml.LookAt(lon, lat, 3473786, 17.8, 179)
  nvp = CreateLonLat(lon, lat)
  desc = '$[name] includes the Austrialian mainland, ' \
         'New Guinea, and Tasmania.'
  SetFeatureFields('pm0', placemark, 'Australia', desc, view, styurl, nvp)

  networklink = kml.genxml.NetworkLink()
  lon = 138.3
  lat = -86.37
  view = kml.genkml.LookAt(lon, lat, 4715247, 0, -140.8)
  nvp = CreateLonLat(lon, lat)
  desc = '$[name] is the Earth\'s southernmost continent and covers ' \
         'the South Pole.'
  SetFeatureFields('nl0', networklink, 'Antarctica', desc, view, styurl, nvp)

  folder = kml.genxml.Folder()
  lon = 18.37
  lat = 49.18
  view = kml.genkml.LookAt(lon, lat, 3430622, 19.8, -51.72)
  nvp = CreateLonLat(lon, lat)
  desc = '$[name] is south of the Arctic, north of the Mediterranean ' \
         'east of the Atlantic and west of the Caucasas Mountains'
  SetFeatureFields('f0', folder, 'Europe', desc, view, styurl, nvp)

  document = kml.genxml.Document()
  lon = 13.15
  lat = -1.01
  view = kml.genkml.LookAt(lon, lat, 5641142, 10.9, 27.13)
  nvp = CreateLonLat(lon, lat)
  desc = '$[name] is the world\'s second largest continent and is ' \
         'the second most populous continent'
  SetFeatureFields('d0', document, 'Africa', desc, view, styurl, nvp)

  groundoverlay = kml.genxml.GroundOverlay()
  lon = -67.09
  lat = -22.48
  view = kml.genkml.LookAt(lon, lat, 5641142, 15.1, 41.21)
  nvp = CreateLonLat(lon, lat)
  desc = '$[name] is east of the Pacific and west of the Atlantic'
  SetFeatureFields('go0', groundoverlay, 'South America', desc, view, styurl, nvp)

  screenoverlay = kml.genxml.ScreenOverlay()
  lon = 102
  lat = 33.7
  view = kml.genkml.LookAt(lon, lat, 4715247, 0, 9.87)
  nvp = CreateLonLat(lon, lat)
  desc = '$[name] is the world\'s largest continent in both land ' \
         'area and population.'
  SetFeatureFields('so0', screenoverlay, 'Asia', desc, view, styurl, nvp)

  photooverlay = kml.genxml.PhotoOverlay()
  lon = -100.7
  lat = 31.7
  view = kml.genkml.LookAt(lon, lat, 4193430, 15.44, 4.72)
  nvp = CreateLonLat(lon, lat)
  desc = '$[name] is south of the Artic and north of the Carribean'
  SetFeatureFields('po0', photooverlay, 'North America', desc, view, styurl, nvp)

  d = kml.genxml.Document()
  d.name = 'Life of a Feature'
  d.open = 1
  d.Add_Style(style.xml())
  d.Add_Feature(placemark.xml())
  d.Add_Feature(networklink.xml())
  d.Add_Feature(folder.xml())
  d.Add_Feature(document.xml())
  d.Add_Feature(groundoverlay.xml())
  d.Add_Feature(screenoverlay.xml())
  d.Add_Feature(photooverlay.xml())

  k = kml.genxml.Kml()
  k.Feature = d.xml()

  return k

k = CreateLOAF()
f = open(loafkml, 'w')
f.write(k.xml())
f.close()
