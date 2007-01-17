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

  def __init__(self):
    self.__node_handler = None
    self.__verbose = False

  def SetNodeHandler(self, node_handler):
    self.__node_handler = node_handler

  def SetVerbose(self, verbose):
    self.__verbose = verbose

  def Walk(self, kmlfile, llab=None, lod=None):

    if self.__verbose:
      print kmlfile

    href = kml.href.Href()
    href.SetUrl(kmlfile)

    kp = kml.kmlparse.KMLParse(kmlfile)
    doc = kp.Doc()
    if not doc:
      print kmlfile,'load or parse error'
      return

    self.__node_handler.HandleNode(href, doc, llab, lod)

    networklink_nodelist = doc.getElementsByTagName('NetworkLink')
    for networklink_node in networklink_nodelist:
      (llab,lod) = GetNetworkLinkRegion(networklink_node)
      child_href = GetNetworkLinkHref(networklink_node)
      child_url = kml.href.ComputeChildUrl(kmlfile, child_href)
      self.Walk(child_url, llab, lod)

