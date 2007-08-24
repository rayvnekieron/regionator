#!/usr/bin/python

# Life of a Link

# A demonstration of elements and behaviors common to all users of LinkType
# See <Link> in the KML reference for detailed information about Link
# http://code.google.com/apis/kml/documentation/kml_tags_beta1.html#link

# NetworkLink's Url/Link, Overlay's Icon, and Model's Link are each of LinkType

import kml.genxml

loalkml = 'life-of-a-link.kml'


def CreatePlacemarkModel(lon, lat, link):
  """ Create the Geometry-specific (Model) part of a Placemark """
  placemark = kml.genxml.Placemark()
  model = kml.genxml.Model()
  model.Link = link.xml()
  location = kml.genxml.Location()
  location.latitude = lat
  location.longitude = lon
  model.Location = location.xml()
  placemark.Geometry = model.xml()
  return placemark

def CreateNetworkLink(link):
  """ Create a NetworkLink with a Url """
  networklink = kml.genxml.NetworkLink()
  networklink.Link = link.xml()
  return networklink

def CreateGroundOverlay(n,s,e,w,icon):
  """ Create a GroundOverlay with an Icon """
  groundoverlay = kml.genxml.GroundOverlay()
  latlonbox = kml.genxml.LatLonBox()
  latlonbox.north = n
  latlonbox.south = s
  latlonbox.east = e
  latlonbox.west = w
  groundoverlay.LatLonBox = latlonbox.xml()
  groundoverlay.Icon = icon.xml()
  return groundoverlay

def SetBasicLinkFields(link, href):
  """ The most basic use of Link simple fetches the URL once """
  link.href = href
  link.viewRefreshMode = 'never' # same as default
  link.refreshMode = 'onChange' # same as default
  return link

def CreateLOAL():
  # Create a Link to a .dae for Placemark's Model
  lon = -120
  lat = 37
  daefile = 'http://kml-samples.googlecode.com/svn/trunk/kml/Model/ResourceMap/shared-textures/geometry/bldg.dae'
  link = kml.genxml.Link()
  SetBasicLinkFields(link, daefile)
  placemark_model = CreatePlacemarkModel(lon, lat, link)

  # Create a Url to a .kml for NetworkLink
  kmlfile = 'http://kml-samples.googlecode.com/svn/trunk/kml/feature-anchor/eat-at-google.kml'
  url = kml.genxml.Url()
  SetBasicLinkFields(url, kmlfile)
  networklink = CreateNetworkLink(url)

  # Create an Icon to a .jpg for GroundOverlay
  n = 37
  s = 36
  e = -110
  w = -120
  imgfile = 'http://kml-samples.googlecode.com/svn/trunk/kml/Model/ResourceMap/photos/bh-flowers.jpg'
  icon = kml.genxml.Icon()
  icon.href = imgfile
  SetBasicLinkFields(icon, imgfile)
  groundoverlay = CreateGroundOverlay(n, s, e, w, icon)

  d = kml.genxml.Document()
  d.name = 'Life of a Link - basic'
  d.open = 1
  d.Add_Feature(placemark_model.xml())
  d.Add_Feature(networklink.xml())
  d.Add_Feature(groundoverlay.xml())

  k = kml.genxml.Kml()
  k.Feature = d.xml()

  return k

k = CreateLOAL()
f = open(loalkml, 'w')
f.write(k.xml())
f.close()

