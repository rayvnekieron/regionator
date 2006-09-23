#!/usr/bin/python

import kml.genxml
import kml.genkml

style0 = '<Style id="style0"/>\n'
style1 = '<Style id="style1"/>\n'

placemark0 = '<Placemark id="placemark0"/>\n'
placemark1 = '<Placemark id="placemark1"/>\n'

timestamp0 = '<TimeStamp id="timestamp0"/>\n'

region0 = '<Region id="region0"/>\n'

schema0 = '<Schema id="schema0"/>\n'
schema1 = '<Schema id="schema1"/>\n'

link = kml.genxml.Link()
link.id = 'link0'
link.href = 'http://foo.com/foo.kml'
networklink = kml.genxml.NetworkLink()
networklink.id = 'networklink0'
networklink.Link = link.xml()

document = kml.genxml.Document()
document.id = 'document0'
document.name = 'my document'
document.Add_Feature(placemark0)
document.Add_Style(style0)
document.Add_Schema(schema0)
document.Add_Feature(placemark1)
document.Add_Schema(schema1)
document.Add_Style(style1)
document.Region = region0
document.TimePrimitive = timestamp0
document.Add_Feature(networklink.xml())

placemark = kml.genxml.Placemark()
placemark.name = 'my placemark'
placemark.id = 'placemark123'

document.Add_Feature(placemark.xml())

latlonaltbox = kml.genxml.LatLonAltBox()
latlonaltbox.north = 50
latlonaltbox.south = 20
latlonaltbox.east = -80
latlonaltbox.west = -120

lod = kml.genxml.Lod()
lod.minLodPixels = 123
lod.maxLodPixels = 4567

region = kml.genxml.Region()
region.LatLonAltBox = latlonaltbox.xml()
region.Lod = lod.xml()

document.Region = region.xml()

folder = kml.genxml.Folder()

r2xml = kml.genkml.Region(2,1,4,3)
folder.Region = r2xml

rbnlxml = kml.genkml.RegionNetworkLink(6,5,8,7,'rbnl','href',123,456)
folder.Add_Feature(rbnlxml)


placemark = kml.genxml.Placemark()
placemark.name = 'point placemark'
point = kml.genxml.Point()
point.coordinates = '10,10'
placemark.Geometry = point.xml()

folder.Add_Feature(placemark.xml())


placemark = kml.genxml.Placemark()
placemark.name = 'linestring placemark'
linestring = kml.genxml.LineString()
linestring.coordinates = '10,10 20,10 10,20 10,10'
placemark.Geometry = linestring.xml()

folder.Add_Feature(placemark.xml())

href = 'http://foo.com/foo.jpg'
groundoverlaykml = kml.genkml.GroundOverlay(10,-10,10,-10,href,42)

folder.Add_Feature(groundoverlaykml)

sokml = kml.genkml.ScreenOverlay('rect',None,2,10,20,30,40, color='ff00ff00')
document.Add_Feature(sokml)

sokml = kml.genkml.ScreenOverlay('img','foo.jpg',1,5,6,7,8)
document.Add_Feature(sokml)

regionkml = kml.genkml.Region(9,8,7,6)
sokml = kml.genkml.ScreenOverlay('rr',None,2,10,20,30,40,
                                  color='ff00ff00', region=regionkml)
document.Add_Feature(sokml)


document.Add_Feature(folder.xml())

document.LookAt = kml.genkml.LookAt(1,2,3,4,5,'id','lookat0')

style = kml.genxml.Style()

iconstyle = kml.genxml.IconStyle()
iconstyle.scale = '1.2'
icon = kml.genxml.Icon()
icon.href = 'icon.jpg'
iconstyle.icon = icon.xml()
hotspot = kml.genxml.hotSpot()
hotspot.xunits = 'pixels'
hotspot.x = 2
hotspot.y = 4
hotspot.yunits = 'pixels'
iconstyle.hotSpot = hotspot.xml()
iconstyle.color = '7f112233'
style.IconStyle = iconstyle.xml()

linestyle = kml.genxml.LineStyle()
linestyle.color = '44332211'
linestyle.width = 2
style.LineStyle = linestyle.xml()

polystyle = kml.genxml.PolyStyle()
polystyle.fill = '1'
polystyle.color = '11223344'
polystyle.outline = '1'
style.PolyStyle = polystyle.xml()

labelstyle = kml.genxml.LabelStyle()
labelstyle.color = '20304050'
labelstyle.scale = '2.3'
style.LabelStyle = labelstyle.xml()

liststyle = kml.genxml.ListStyle()
liststyle.listItemType = 'radioFolder'
style.ListStyle = liststyle.xml()

balloonstyle = kml.genxml.BalloonStyle()
balloonstyle.bgColor = 'ffff0000'
balloonstyle.textColor = 'ff0000ff'
balloonstyle.text = 'balloon text'
style.balloonstyle = balloonstyle.xml()

document.Add_Style(style.xml())

k = kml.genxml.Kml()
k.comment = '<!-- this is my comment -->\n'
k.Feature = document.xml()
update = '<Change/>'
targethref = 'http://foo.com/goo.py'
nlc = kml.genkml.NetworkLinkControl('cookie','expires', update, targethref)
k.NetworkLinkControl = nlc

f = open('testkml.kml','w')
f.write(k.xml())
f.close()
