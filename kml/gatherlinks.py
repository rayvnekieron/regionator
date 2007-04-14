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

import getopt
import md5
import sys
import kml.walk
import kml.href


class LinkGatheringNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self, opts):
    self.__links = {}
    self.__gather_kml = False
    self.__gather_html = False
    self.__gather_relative = False
    self.__gather_absolute = False

    opts, args = getopt.getopt(opts, "khrv")
    for o,a in opts:
      if o == '-k':
        self.__gather_kml = True
      elif o == '-h':
        self.__gather_html = True
      elif o == '-r':
        self.__gather_relative = True
      elif o == '-a':
        self.__gather_absolute = True

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
    description_nodelist = node.getElementsByTagName('description')
    for description_node in description_nodelist:
      cdata = kml.kmlparse.GetCDATA(description_node)
      # The HTML typically found here is not well structured enough to dom parse
      # so we dig through the CDATA as a raw string.
      href_list = cdata.split('href="') # as in <a href="http://foo.com/hi">
      for n in href_list[1:]: # [0] is the stuff before the first 'href'
        end_quote = n.find('"')
        self._SaveLink(parent, n[0:end_quote])
      src_list = cdata.split('src="') # as in <img src="foo.jpg">
      for n in src_list[1:]: # [0] is the stuff before the first 'src'
        end_quote = n.find('"')
        self._SaveLink(parent, n[0:end_quote])

  # kml.walk.KMLNodeHandler:HandleNode()
  def HandleNode(self, href, node, llab, lod):
    parent = href.Href()
    href_nodelist = node.getElementsByTagName('href')
    for href_node in href_nodelist:
      child = kml.kmlparse.GetText(href_node)
      self._SaveLink(parent, child)
    if self.__gather_html:
      self._GatherHtmlLinks(parent, node)



def GatherLinks(opts, kmlurl):
  link_gathering_node_handler = LinkGatheringNodeHandler(opts)
  hier = kml.walk.KMLHierarchy()
  hier.SetNodeHandler(link_gathering_node_handler)
  hier.Walk(kmlurl)
  return link_gathering_node_handler.Links()

