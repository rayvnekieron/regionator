#!/usr/bin/python

import kml.genxml

style0 = '<Style id="style0"/>\n'
style1 = '<Style id="style1"/>\n'

placemark0 = '<Placemark id="placemark0"/>\n'
placemark1 = '<Placemark id="placemark1"/>\n'

timestamp0 = '<TimeStamp id="timestamp0"/>\n'

region0 = '<Region id="region0"/>\n'

schema0 = '<Schema id="schema0"/>\n'
schema1 = '<Schema id="schema1"/>\n'

link = kml.genxml.Link()
link.href = 'http://foo.com/foo.kml'
networklink = kml.genxml.NetworkLink()
networklink.Link = link.xml()

document = kml.genxml.Document()
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

k = kml.genxml.Kml()
k.comment = '<!-- this is my comment -->\n'
k.Feature = document.xml()

f = open('testkml.kml','w')
f.write(k.xml())
f.close()
