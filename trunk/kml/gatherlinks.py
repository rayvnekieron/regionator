"""
Copyright (C) 2007 Google Inc.

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

import md5
import sys
import kml.walk
import kml.href
import kml.kmlgetopt


class LinkGatheringNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self, go):
    self.__links = {}
    self.__gather_kml = go.Get('k')
    self.__gather_html = go.Get('h')
    self.__gather_relative = go.Get('r')
    self.__gather_absolute = go.Get('a')

  def SetRoot(self, root):
    self.__root = root

  def Links(self):
    return self.__links

  def _SaveLink(self, parent, child):
    # Skip empty hrefs
    if not child:
      return

    # href's are often just a hostname (www.foo.com).  This converts
    # these to an absolute URL.
    if kml.href.IsHostname(child):
      # Make child an absolute URL:
      child = 'http://' + child

    if kml.href.IsRelative(child):
      if not self.__gather_relative:
        return
    else:
      if not self.__gather_absolute:
        return

    # Compute the absolute URL.
    url = kml.href.ComputeChildUrl(parent, child)
    if self.__links.has_key(url):
      self.__links[url] += 1
    else:
      self.__links[url] = 1

  def _GatherHtmlLinks(self, parent, node):
    links = kml.walk.GetHtmlLinksInNode(node)
    for link in links:
      self._SaveLink(parent, link)

  # kml.walk.KMLNodeHandler:HandleNode()
  def HandleNode(self, href, node, llab, lod):
    parent = href.Href()
    href_nodelist = node.getElementsByTagName('href')
    for href_node in href_nodelist:
      child = kml.kmlparse.GetText(href_node)
      self._SaveLink(parent, child)
    if self.__gather_html:
      self._GatherHtmlLinks(parent, node)


def ParseArgv(argv):
  return kml.kmlgetopt.Getopt(argv, 'khare:u:')


def GatherLinks(argv):
  go = ParseArgv(argv)
  link_gathering_node_handler = LinkGatheringNodeHandler(go)
  hier = kml.walk.KMLHierarchy()
  hier.SetNodeHandler(link_gathering_node_handler)
  enc = go.Get('e')
  if enc:
    hier.SetEncoding(enc)
  if not hier.Walk(go.Get('u')):
    return None
  return link_gathering_node_handler.Links()


def PrintLinks(link_map):
  """Print all links in the dictionary
  Args:
    links: a map of link names to reference count
  """
  link_list = []
  for link in link_map.keys():
    link_list.append(link)
  link_list.sort()
  for link in link_list:
    print link,link_map[link]

def GatherAndPrintLinks(opts, kmlurl):
  map = GatherLinks(opts, kmlurl)
  PrintLinks(map)
