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


def ParseRegion(region_node):
  (llab_node, lod_node) = kml.kmlparse.ParseRegion(region_node)
  llab = kml.kmlparse.ParseLatLonAltBox(llab_node)
  lod = kml.kmlparse.ParseLod(lod_node)
  return (llab, lod)


def GetNetworkLinkRegion(networklink_node):
  region_nodelist = networklink_node.getElementsByTagName('Region')
  if region_nodelist:
    return ParseRegion(region_nodelist[0])
  return (None, None)


def GetLinkHref(link_node):
  link = kml.kmlparse.ParseLink(link_node)
  return link.href


def GetNetworkLinkHref(networklink_node):
  link = kml.kmlparse.GetFirstChildElement(networklink_node, 'Link')
  if not link:
    link = kml.kmlparse.GetFirstChildElement(networklink_node, 'Url')
  if link:
    return GetLinkHref(link)
  return None


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

  def Walk(self, kmlfile, llab=None, lod=None):
    """
    Args:
      kmlfile: pathname or URL to top of KML hierarchy
      llab: LatLonAltBox of parent
      lod: Lod of parent
    Returns:
      True: kmlfile and all immediate children exists and parses
      False: kmlfile or child does not exist or fails to parse
    """
    if self.__verbose:
      print kmlfile

    href = kml.href.Href()
    href.SetUrl(kmlfile)

    kp = kml.kmlparse.KMLParse(kmlfile)
    doc = kp.Doc()
    if not doc:
      if self.__verbose:
        print kmlfile,'load or parse error'
      return False

    if not self.__node_handler:
      return False

    self.__node_handler.HandleNode(href, doc, llab, lod)

    my_status = True
    networklink_nodelist = doc.getElementsByTagName('NetworkLink')
    for networklink_node in networklink_nodelist:
      (llab,lod) = GetNetworkLinkRegion(networklink_node)
      child_href = GetNetworkLinkHref(networklink_node)
      child_url = kml.href.ComputeChildUrl(kmlfile, child_href)
      child_status = self.Walk(child_url, llab, lod)
      if child_status == False:
        my_status = False

    return my_status


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
  


