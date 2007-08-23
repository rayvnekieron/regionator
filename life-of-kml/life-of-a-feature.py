#!/usr/bin/python

# Life of a Feature
#
# A demonstration of KML elements and behavior common to all Features

import kml.genxml
import sys

loafkml = 'life-of-a-feature.kml'

def CreateStyle(id):

  balloonstyle = kml.genxml.BalloonStyle()
  text = []
  text.append('<b>$[name]</b>')
  text.append('$[description]')
  text.append('<i>$[id]</i>')
  balloonstyle.text = '<br/>'.join(text)
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
    data.value = id
    extendeddata.Add_Data(data.xml())
  return extendeddata

def SetFeatureStuff(feature, short, long, id, style_url, nvp_list):
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
  # feature.AbstractView
  # feature.TimePrimitive
  feature.styleUrl = style_url
  # feature.StyleSelector
  # feature.Region
  # feature.ExtendedData = CreateExtendedData(nvp_list)

def CreateLOAF():
  style_id = 'shared-style'
  style_url = '#%s' % style_id

  style = CreateStyle(style_id)

  placemark = kml.genxml.Placemark()
  SetFeatureStuff(placemark, 'PM', 'Placemark', 'pm0', style_url, None)

  networklink = kml.genxml.NetworkLink()
  SetFeatureStuff(networklink, 'NL', 'NetworkLink', 'nl0', style_url, None)

  folder = kml.genxml.Folder()
  SetFeatureStuff(folder, 'F', 'Folder', 'f0', style_url, None)

  document = kml.genxml.Document()
  SetFeatureStuff(document, 'D', 'Document', 'd0', style_url, None)

  groundoverlay = kml.genxml.GroundOverlay()
  SetFeatureStuff(groundoverlay, 'GO', 'GroundOverlay', 'go0', style_url, None)

  screenoverlay = kml.genxml.ScreenOverlay()
  SetFeatureStuff(screenoverlay, 'SO', 'ScreenOverlay', 'so0', style_url, None)

  photooverlay = kml.genxml.PhotoOverlay()
  SetFeatureStuff(photooverlay, 'PO', 'PhotoOverlay', 'po0', style_url, None)

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
