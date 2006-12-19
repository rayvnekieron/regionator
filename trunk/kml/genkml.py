"""
Copyright (C) 2006 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
$URL$
$Revision$
$Date$
"""

""" Generate KML

Convenience functions to generate KML fragments.

"""

import kml.genxml


def Point(lon,lat,attrname=None,attrval=None):

  """<Point [attrname=attrval]><coordinates>

  Args:
    lon,lat: decimal degrees, float
    attrname: id or targetId
    attrval: string

  Returns:
    KML: <Point>...

  """

  point = kml.genxml.Point()
  point.coordinates = '%f,%f' % (lon,lat)

  return point.xml()


def Placemark(geometry,name=None,styleurl=None,attrname=None,attrval=None):

  """<Placemark>...</Placemark>

  Args:
    geometry: string: <Point>,<LineString>,<Polygon>,<MultiGeometry>
    name: string: <name>
    style: string: <Style> or <styleUrl>

  Returns:
    KML: <Placemark>...</Placemark>
  """

  placemark = kml.genxml.Placemark()
  if name:
    placemark.name = name
  if styleurl:
    placemark.styleurl = styleurl
  placemark.Geometry = geometry
  return placemark.xml()


def PlacemarkPoint(lon,lat,name):

  """<Placemark><Point>...</Point></Placemark>

  Args:
    lon,lat:
    name: <name>

  Returns:
    KML: <Placemark><Point>...</Point></Placemark>
  """ 

  return Placemark(Point(lon,lat),name=name)


def LineStyle(a,b,g,r,width=1.0):

  """<LineStyle>...</LineStyle>
  """

  linestyle = kml.genxml.LineStyle()
  linestyle.color = '%02x%02x%02x%02x' % (a,b,g,r)
  linestyle.width = repr(width)
  return linestyle.xml()


def PolyStyle(a,b,g,r,fill,outline):

  """<PolyStyle>...</PolyStyle>
  """

  polystyle = kml.genxml.PolyStyle()
  polystyle.color = '%02x%02x%02x%02x' % (a,b,g,r)
  polystyle.fill = repr(fill)
  polystyle.outline = repr(outline)
  return polystyle.xml()


def ListStyle(listItemType):

  """<ListStyle>...</ListStyle>

  Args:
    listItemType: 'check', 'checkOffOnly', 'checkHideChildren', 'radioFolder'

  Returns:
    KML: <ListStyle>...</ListStyle>
  """

  liststyle = kml.genxml.ListStyle()
  liststyle.listItemType = listItemType
  return liststyle.xml()


def CheckHideChildren(id=None):

  """<Style><ListStyle>...</ListStyle></Style>

  Helper function to create the appropriate KML to hide the children of
  either a Document, Folder or NetworkLink.

  NOTE: In a Folder or NetworkLink this is an inline style.  In a Document
  this is a shared style and the Document must also use a <styleUrl> to
  reference this Style for the ListStyle to take effect.

  Args:
    id: unique string

  Returns:
    KML: <Style><ListStyle><listItemType>checkHideChildren...</Style>
  """

  style = kml.genxml.Style()
  if id:
    style.id = id
  style.ListStyle = ListStyle('checkHideChildren')
  return style.xml()


def PolygonBox(n,s,e,w,alt):

  """<Polygon>...</Polygon>

  Polygon with corners at nw,ne,se,sw

  Returns:
    KML: <Polygon>...</Polygon>
  """

  coordinates = Coordinates()
  coordinates.AddPoint(w,n,alt)
  coordinates.AddPoint(e,n,alt)
  coordinates.AddPoint(e,s,alt)
  coordinates.AddPoint(w,s,alt)
  coordinates.AddPoint(w,n,alt)
  linearring = kml.genxml.LinearRing()
  linearring.coordinates = coordinates.Coordinates()

  outer = kml.genxml.outerBoundaryIs()
  outer.LinearRing = linearring.xml()

  polygon = kml.genxml.Polygon()
  polygon.outerBoundaryIs = outer.xml()

  return polygon.xml()


def LineStringBox(n,s,e,w):

  """<LineString>

  LineString between nw,ne,se,sw,nw.

  Tessellated to follow terrain and curvature of the earth.

  Returns:
    KML: <LineString>...</LineString>
  """

  c = Coordinates()
  c.AddPoint2(w,n)
  c.AddPoint2(e,n)
  c.AddPoint2(e,s)
  c.AddPoint2(w,s)
  c.AddPoint2(w,n)

  linestring = kml.genxml.LineString()
  linestring.coordinates = c.Coordinates()
  linestring.tessellate = 1

  return linestring.xml()


def LineStringAltBox(n,s,e,w,alt,altMode='relativeToGround'):

  """<LineString>

  LineString between nw,ne,se,sw,nw at altitude alt.

  Args:
    n,s,e,w: float
    alt: altitude
    altMode: relativeToGround (default) or absolute

  Returns:
    KML: <LineString>...</LineString>
  """

  c = Coordinates()
  c.AddPoint(w,n,alt)
  c.AddPoint(e,n,alt)
  c.AddPoint(e,s,alt)
  c.AddPoint(w,s,alt)
  c.AddPoint(w,n,alt)

  linestring = kml.genxml.LineString()
  linestring.coordinates = c.Coordinates()
  linestring.altitudeMode = altMode

  return linestring.xml()


def Box(n,s,e,w,name,styleurl=None,alt=None,altMode='relativeToGround'):

  """<Placemark><LineString>...</LineString></Placemark>

  Returns a Placemark with a LineString box between the corners of the
  given bounding box.

  Args:
    n,s,e,w: float
    name: Placemark name
    styleurl: <styleUrl> xml string
    alt: altitude
    altMode: relativeToGround or absolute (only if alt != 0)

  Returns:
    KML: <Placemark><LineString>...</LineString></Placemark>
  """

  placemark = kml.genxml.Placemark()
  placemark.name = name
  if styleurl:
    placemark.styleUrl = styleurl
  if alt:
    placemark.Geometry = LineStringAltBox(n,s,e,w,alt,altMode)
  else:
    placemark.Geometry = LineStringBox(n,s,e,w)
  return placemark.xml()


def RegionBox(name,n,s,e,w,minpx,maxpx):

    """ <Placemark><Region>...</Region><LineString>...</LineString></Placemark>

    Args:
      n,s,e,w: float
      minpx,maxpx: minLodPixels, maxLodPixels

    Returns:
      KML: <Placemark><Region>...</Region><LineString>...</LineString></Placemark>
    """

    placemark = kml.genxml.Placemark()
    placemark.name = name
    regionxml = kml.genkml.Region(n,s,e,w,minpx=minpx,maxpx=maxpx)
    boxxml = kml.genkml.LineStringBox(n,s,e,w)
    placemark.Geometry = boxxml
    placemark.Region = regionxml
    return placemark.xml()


def LatLonOutline(n,s,e,w,name):

  """ Generate a lat-lon-aligned box

  A filled Polygon with 0 opacity with outline enabled traces
  the lat-lon-aligned border of the given bounding box.

  (A KML LineString with corner coordinates using pairings of
  n,s,e,w has line segments which trace the shortest distance
  between the two corners -- this does not follow a longitude line).

  NOTE: The object will be not be visible if a GroundOverlay
  covers the same area because the draw order of this
  filled polygon is less than any GroundOverlay.

  Args:
    n,s,e,w: lat-lon-aligned bounding box
    name: string used in <name> for this object

  Returns:
    KML Placemark
  """

  style = kml.genxml.Style()
  style.PolyStyle = PolyStyle(0,0,0,0,1,1)
  style.LineStyle = LineStyle(255,255,255,255,2.0)
  placemark = kml.genxml.Placemark()
  placemark.name = name
  placemark.Add_Style(style.xml())
  placemark.Geometry = PolygonBox(n,s,e,w,0)
  return placemark.xml()


def LatLonBox(n,s,e,w):

  """<LatLonBox>...</LatLonBox>
  """

  latlonbox = kml.genxml.LatLonBox()
  latlonbox.Set_NSEW(n,s,e,w)
  return latlonbox.xml()


def Region(n,s,e,w,minalt=0,maxalt=0,minpx=128,minfade=0,maxpx=1024,maxfade=0):

  """<Region>...</Region>

  Args:
    NOTE: all args are _string_ representations of the floating point values
    n,s,e,w: geographic bounding box
    minalt,maxalt: minAltitude,maxAltitude
    minpx,maxpx: minLodPixels,maxLodPixels
    minfade,maxfade: minFadePixels,maxFadePixels
  """

  latlonaltbox = kml.genxml.LatLonAltBox()
  latlonaltbox.north = n
  latlonaltbox.south = s
  latlonaltbox.east = e
  latlonaltbox.west = w
  if minalt:
    latlonaltbox.minAltitude = minalt
  if maxalt:
    latlonaltbox.maxAltitude = maxalt

  lod = kml.genxml.Lod()
  lod.minLodPixels = minpx
  lod.maxLodPixels = maxpx

  region = kml.genxml.Region()
  region.LatLonAltBox = latlonaltbox.xml()
  region.Lod = lod.xml()

  return region.xml()


def RegionLod(n,s,e,w,minpx,maxpx):

  """<Region>...</Region>

  Region with default min/maxAltitude and no fade extents

  """

  return Region(n,s,e,w,0,0,minpx,0,maxpx,0)


def RegionNetworkLink(n,s,e,w,name,href,minpx,maxpx):

  """<NetworkLink><Region>...</Region></NetworkLink>

  Region-based NetworkLink, onRegion viewRefreshMode.

  """

  regionxml = Region(n,s,e,w,minpx=minpx,maxpx=maxpx)

  link = kml.genxml.Link()
  link.href = href
  link.viewRefreshMode = 'onRegion'

  networklink = kml.genxml.NetworkLink()
  networklink.name = name
  networklink.Link = link.xml()
  networklink.Region = regionxml

  return networklink.xml()


def GroundOverlay(n,s,e,w,href,draworder,region=None):

  """<GroundOverlay>...</GroundOverlay>

  """

  icon = kml.genxml.Icon()
  icon.href = href
  latlonboxkml = LatLonBox(n,s,e,w)
  groundoverlay = kml.genxml.GroundOverlay()
  groundoverlay.drawOrder = draworder
  groundoverlay.Icon = icon.xml()
  groundoverlay.LatLonBox = latlonboxkml
  if region:
    groundoverlay.Region = region
  return groundoverlay.xml()


def RegionGroundoverlay(n,s,e,w,minpx,maxpx,href,draworder):

  """<GroundOverlay><Region>
  """

  region = Region(n,s,e,w,minpx=minpx,maxpx=maxpx)
  return GroundOverlay(n,s,e,w,href,draworder,region)

def NetworkLink(href):

  """<NetworkLink>...</NetworkLink>
  """

  networklink = kml.genxml.NetworkLink()
  networklink.name = href
  link = kml.genxml.Link()
  link.href = href
  networklink.Link = link.xml()
  return networklink.xml()


def ScreenOverlay(name,href,draworder,x,y,wid,ht,color=None,region=None):

  """<ScreenOverlay>...</ScreenOverlay>

  Draw the given image at the given location and size
  on the screen.

  Args:
    name: string for <name>
    href: url/filename for <href>
    draworder: int for <drawOrder>
    x,y: screen coord relative to lower-left
    wid,ht: screen dimensions of image
    region: <Region>

  Returns:
    KML: <ScreenOverlay>...</ScreenOverlay>
  """

  screenoverlay = kml.genxml.ScreenOverlay()
  screenoverlay.name = name

  if color:
    screenoverlay.color = color

  if region:
    screenoverlay.Region = region
  screenoverlay.drawOrder = draworder

  if href:
    icon = kml.genxml.Icon()
    icon.href = href
    screenoverlay.Icon = icon.xml()

  overlayxy = kml.genxml.overlayXY()
  overlayxy.x = 0
  overlayxy.y = 0
  overlayxy.xunits = 'pixels'
  overlayxy.yunits = 'pixels'
  screenoverlay.overlayXY = overlayxy.xml()

  screenxy = kml.genxml.screenXY()
  screenxy.x = x
  screenxy.y = y
  screenxy.xunits = 'pixels'
  screenxy.yunits = 'pixels'
  screenoverlay.screenXY = screenxy.xml()

  size = kml.genxml.size()
  size.x = wid
  size.y = ht
  screenoverlay.size = size.xml()

  return screenoverlay.xml()


def ScreenOverlayRect(name,color,draworder,x,y,wid,ht,region=None):

  """<ScreenOverlay>...</ScreenOverlay>

  A ScreenOverlay with no Icon draws a rectangle on the screen.

  Args:
    name: string for <name>
    color: hex abgr for <color>
    draworder: int for <drawOrder>
    x,y: screen coord relative to lower-left
    wid,ht: screen dimensions of image
    region: <Region>

  Returns:
    KML: '<ScreenOverlay>...</ScreenOverlay>'
  """

  return ScreenOverlay(name,None,draworder,x,y,wid,ht,color=color,region=region)


def TimeSpan(b, e):

  """<TimeSpan>...</TimeSpan>

  Args:
    begin: string
    end: string

  Returns:
    KML: <TimeSpan>...</TimeSpan>
  """ 

  timespan = kml.genxml.TimeSpan()
  timespan.begin = b
  timespan.end = e
  return timespan.xml()


def TimeStamp(when):

  """<TimeStamp>...</TimeStamp>

  Args:
    when: string

  Returns:
    KML: <TimeStamp>...</TimeStamp>
  """ 

  timestamp = kml.genxml.TimeStamp()
  timestamp.when = when
  return timestamp.xml()


def Update(update,targethref):

  """<Update><targetHref>

  Args:
    update: <Create|Delete|Change>... />
    targethref: <targetHref> value

  Returns:
    KML: <Update><targetHref>...<Create|Delete|Change>...</Update>
  """

  u = []
  u.append('<Update>\n')
  u.append('<targetHref>%s</targetHref>\n' % targethref)
  u.append(update)
  u.append('</Update>\n')
  return "".join(u)


def NetworkLinkControl(cookie=None,expires=None,update=None,targethref=None):

  """<NetworkLinkControl>

  [Other NLC tags not used here include:
    <minRefreshPeriod>,<message>
    <linkName>,<linkDescription>,<linkSnippet>]

  Args:
    expires: <expires> value, ISO 8601
    cookie: <cookie> value, must be name=value
    targethref: <targetHref> value
    update: body of <Update> (targetHref must be supplied)

  Returns:
    KML: <NetworkLinkControl>
  """

  nlc = kml.genxml.NetworkLinkControl()
  if nlc:
    nlc.cookie = cookie
  if expires:
    nlc.expires = expires
  if update and targethref:
    nlc.Update = Update(update,targethref)
  return nlc.xml()


def LookAt(lon,lat,range,tilt,heading,attrname=None,attrval=None):

  """<Lookat [attrname=attrval]>

  Args:
    lon: <longitude> float
    lat: <latitude> float
    range: <range> float
    tilt: <tilt> float
    heading: <heading> float
    attrname: attribute name ('id' or 'targetId')
    attrval: attribute value string

  Returns:
    KML: <LookAt>...</LookAt>
  """

  lookat = kml.genxml.LookAt()
  if attrname == 'id':
    lookat.id = attrval
  elif attrname == 'targetId':
    lookat.targetId = attrval
  if lon:
    lookat.longitude = '%f' % lon
  if lat:
    lookat.latitude = '%f' % lat
  if range:
    lookat.range = '%f' % range
  if tilt:
    lookat.tilt = '%f' % tilt
  if heading:
    lookat.heading = '%f' % heading
  return lookat.xml()


class Coordinates:

  """Create <coordinates> data

  1) create Coordinates()
  2) SetPoint() or N x AddPoint()
  3) Coordinates() returns data

  """

  def __init__(self):
    self.__coordinates = []


  def SetPoint2(self, lon, lat):

    """
    Args:
      lon,lat: float
    """

    self.AddPoint2(lon, lat)


  def SetPoint(self, lon, lat, alt):

    """
    Args:
      lon,lat,alt: float
    """

    self.AddPoint(lon, lat, alt)


  def AddPoint2(self, lon, lat):

    """
    Args:
      lon,lat: float
    """

    if self.__coordinates:
      nl = '\n'
    else:
      nl = ''
    cstr = '%s%f,%f' % (nl, lon, lat)
    self.__coordinates.append(cstr)


  def AddPoint(self, lon, lat, alt):

    """
    Args:
      lon,lat,alt: float
    """

    if self.__coordinates:
      nl = '\n'
    else:
      nl = ''
    cstr = '%s%f,%f,%f' % (nl, lon, lat, alt)
    self.__coordinates.append(cstr)


  def Coordinates(self):

    """
    Returns the set of coordinates as a string

    Returns:
      string:
    """

    return "".join(self.__coordinates)
 
