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

import xml.dom.minidom
import kml.href
import kml.kmlparse

"""

Walk a KML NetworkLink hierarchy.


"""

class KMLNodeHandler:

  def HandleNode(self, href, node, llab, lod):
    """ """


class KMLHierarchy:

  """
  0) Derive a class based on KMLNodeHandler and implement HandleNode
  1) Create a KMLHierarchy instance
  2) SetNodeHandler()
  3) Walk(url)
  """

  def __init__(self):
    self.__node_handler = None
    self.__verbose = False
    self.__encoding = None

  def SetNodeHandler(self, node_handler):
    """
    Args:
      node_handler: kml.walk.KMLNodeHandler
    """
    self.__node_handler = node_handler

  def SetVerbose(self, verbose):
    """
    Args:
      verbose: if True enable output to stdout, if False fully silent
    """
    self.__verbose = verbose

  def SetEncoding(self, encoding):
    """
    Args:
      encoding: override encoding specified in xml header
    """
    self.__encoding = encoding

  def Walk(self, kmlfile, llab=None, lod=None):
    """
    NOTE: Errors with child links are not propagated to the return value.
    Args:
      kmlfile: pathname or URL to top of KML hierarchy
      llab: LatLonAltBox of parent
      lod: Lod of parent
    Returns:
      True: kmlfile and exists and parses
      False: kmlfile does not exist or fails to parse
    """
    if self.__verbose:
      print kmlfile

    href = kml.href.Href()
    href.SetUrl(kmlfile)

    if self.__encoding:
      data = kml.href.FetchUrl(kmlfile)
      (xml_header, xml_data) = kml.kmlparse.SplitXmlHeaderFromData(data)
      kp = kml.kmlparse.KMLParse(None)
      kp.ParseStringUsingCodec(xml_data, self.__encoding)
    else:
      kp = kml.kmlparse.KMLParse(kmlfile)
    doc = kp.Doc()
    if not doc:
      if self.__verbose:
        print kmlfile,'load or parse error'
      return False

    if not self.__node_handler:
      return False

    self.__node_handler.HandleNode(href, doc, llab, lod)

    networklink_nodelist = doc.getElementsByTagName('NetworkLink')
    for networklink_node in networklink_nodelist:
      (llab,lod) = kml.kmlparse.ParseFeatureRegion(networklink_node)
      child_href = kml.kmlparse.GetNetworkLinkHref(networklink_node)
      child_url = kml.href.ComputeChildUrl(kmlfile, child_href)
      # NOTE: Errors on children are not propagated up.
      self.Walk(child_url, llab, lod)

    return True


def GetLinksOfAttr(html_text, attr, link_list):
  # as in <TAG ATTR="http://foo.com/hi">
  attr_list = html_text.split('%s="' % attr)
  for n in attr_list[1:]: # [0] is the stuff before the first 'href'
    end_quote = n.find('"')
    link_list.append(n[0:end_quote])


def GetLinksInHtml(html_text, link_list):
  """Return a list of all links in the HTML
  Looks for <a href="..."> and <img src="...">
  Args:
    html_text: HTML text
  Returns:
    list: list of links
  """
  GetLinksOfAttr(html_text, 'href', link_list)
  GetLinksOfAttr(html_text, 'src', link_list)


def GetHtmlLinksInNode(kml_node):
  link_list = []
  description_nodelist = kml_node.getElementsByTagName('description')
  for description_node in description_nodelist:
    cdata = kml.kmlparse.GetCDATA(description_node)
    kml.walk.GetLinksInHtml(cdata, link_list)
  return link_list
  


