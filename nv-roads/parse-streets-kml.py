#!/usr/bin/python
# XXX better comments coming real soon now...

import os
import re
import sys
import kml.genxml
import kml.genkml
import kml.kmlparse

def GetStreetTypes():
  """Returns a list of street types represented in the shape file
  """
  types = ['ACCESS', 'COLLECTOR', 'HIGHWAY', 'LANE',
           'LOCAL', 'MAJOR', 'MINOR', 'PRIVATE']
  return types


def GetColorWidthLod(street_type):
  """Returns a list of color, width and minLodPixels for a given street type
  """
  d = {
    'ACCESS'    : ['7fff0000', 4, 2048], # blue
    'COLLECTOR' : ['7f336699', 4, 2048], # brown
    'HIGHWAY'   : ['7fffff00', 4, 512],  # cyan
    'LANE'      : ['7f00ff00', 4, 4096], # green
    'LOCAL'     : ['7fff00ff', 4, 8192], # magenta
    'MAJOR'     : ['7f0080ff', 4, 1024], # orange
    'MINOR'     : ['7f800080', 4, 4096], # purple
    'PRIVATE'   : ['7f0000ff', 4, 2048], # red
  }
  return d[street_type]


def GetStreetTypeFromDescription(desc):
  """Parse the description of the linestring placemark and return the street
  type"""
  p = re.compile('<b>CLASSIFICA:</b> <i>([A-Z]*)</i>', re.DOTALL)
  r = p.search(desc)
  street_types = GetStreetTypes()
  return r.group(1)


def CreateStyle(id, color, width):
  """<Style><LineStyle>...<ListStyle>...
  """
  linestyle = kml.genxml.LineStyle()
  linestyle.Set_color(color)
  linestyle.Set_width(width)
  liststyle = kml.genxml.ListStyle()
  liststyle.Set_bgColor(color)
  style = kml.genxml.Style()
  style.Set_id(id)
  style.Set_LineStyle(linestyle.xml())
  style.Set_ListStyle(liststyle.xml())
  return style


def CreateRegion(minlodpx):
  """<Region><LatLonAltBox>...<Lod>...
  """
  n, s, e, w = 49.587, 49.181, -122.750, -123.599
  #region = kml.genkml.RegionLod(n,s,e,w,minlodpx,-1) XXX fix me
  region = kml.genkml.Region(n,s,e,w,0,0,None,minlodpx,-1,0)
  return region


def ParseLineString(linestring_xml):
  placemark = kml.genxml.Placemark()
  linestring = kml.genxml.LineString()
  coords = linestring_xml.getElementsByTagName('coordinates')[0]
  linestring.Set_coordinates(coords.childNodes[0].data)
  placemark.Set_Geometry(linestring.xml())
  return placemark


def main():
  infile = 'streets.kml'
  assert os.access(infile, os.R_OK)
  kmldom = kml.kmlparse.KMLParse(infile).Doc()

  street_types = GetStreetTypes()
  street_type_dict = {}
  for type in street_types:
    street_type_dict[type] = []

  placemark_node_list = kmldom.getElementsByTagName('Placemark')
  for placemark in placemark_node_list:
    description = kml.kmlparse.GetSimpleElementText(placemark, 'description')
    street_type = GetStreetTypeFromDescription(description)
    street_type_dict[street_type].append(placemark)

  for type in street_types:
    doc = kml.genxml.Document()
    doc.Set_name(type.title())
    doc.Set_styleUrl('#%s' % type)
    (color, width, lod) = GetColorWidthLod(type)
    style = CreateStyle(type, color, width)
    doc.Add_Style(style.xml())
    region = CreateRegion(lod)
    doc.Set_Region(region)
    for placemark in street_type_dict[type]:
      kml_linestring = ParseLineString(placemark)
      kml_linestring.Set_styleUrl('#%s' % type)
      doc.Add_Feature(kml_linestring.xml())
    outfile = 'roads-%s.kml' % type.lower()
    f = open(outfile, 'w')
    f.write(doc.xml())
    f.close()
    print 'writing %s...' % outfile
  print 'done'


if __name__ == '__main__':
  main()
