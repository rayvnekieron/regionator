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
import sys
import kml.walk
import kml.href


class LinkCheckingNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self, opts):
    self.__check_kml = False
    self.__check_html = False
    self.__check_absolute = False
    self.__check_relative = False
    self.__verbose = False

    opts, args = getopt.getopt(opts, "khrav")
    for o,a in opts:
      if o == '-k':
        self.__check_kml = True
      elif o == '-h':
        self.__check_html = True
      elif o == '-r':
        self.__check_relative = True
      elif o == '-a':
        self.__check_absolute = True
      elif o == '-v':
        self.__verbose = True

    self.__node_count = 0
    self.__kml_link_count = 0
    self.__html_link_count = 0
    self.__relative_link_count = 0
    self.__absolute_link_count = 0
    self.__empty_link_count = 0
    self.__error_count = 0

  def Status(self):
    return self.__error_count

  def Statistics(self):
    return (self.__node_count,
            self.__kml_link_count,
            self.__html_link_count,
            self.__relative_link_count,
            self.__absolute_link_count,
            self.__empty_link_count,
            self.__error_count)

  def PrintSummary(self):
    self._Print('X  ', '%d nodes' % self.__node_count)
    if self.__check_kml:
      self._Print('X  ','%d kml links' % self.__kml_link_count)
    if self.__check_html:
      self._Print('X  ','%d html links' % self.__html_link_count)
    if self.__check_relative:
      self._Print('X  ','%d relative links' % self.__relative_link_count)
    if self.__check_absolute:
      self._Print('X  ','%d absolute links' % self.__absolute_link_count)
    self._Print('X  ','%d empty links' % self.__empty_link_count)
    self._Print('X  ','%d errors' % self.__error_count)

  def _Print(self, code, data, *more):
    if self.__verbose:
      print code,data,
      for m in more:
        print m,
      print # newline

  def _Fetch(self, parent, child):
    # Handle empty href and count this separately from errors.
    if not child:
      self._Print('ERR','[empty]',parent)
      self.__empty_link_count += 1
      return

    # Count and fetch only if asked to.
    if kml.href.IsRelative(child):
      if not self.__check_relative:
        return
      self.__relative_link_count += 1
    else:
      if not self.__check_absolute:
        return
      self.__absolute_link_count += 1

    # Be verbose only if asked and only about links we're asked to check.
    if self.__verbose:
      self._Print('C  ',child)

    # Compute the absolute URL and try to fetch it.
    url = kml.href.ComputeChildUrl(parent, child)
    self._Print('U  ',url)
    data = kml.href.FetchUrl(url)
    if data:
      self._Print('D  ',len(data))
    else:
      self._Print('ERR',child,parent)
      self.__error_count += 1

  def _CheckHtml(self, parent, node):
    description_nodelist = node.getElementsByTagName('description')
    for description_node in description_nodelist:
      cdata = kml.kmlparse.GetCDATA(description_node)
      # The HTML typically found here is not well structured enough to dom parse
      # so we dig through the CDATA as a raw string.
      href_list = cdata.split('href="') # as in <a href="http://foo.com/hi">
      for n in href_list[1:]: # [0] is the stuff before the first 'href'
        self.__html_link_count += 1
        end_quote = n.find('"')
        self._Fetch(parent, n[0:end_quote])
      src_list = cdata.split('src="') # as in <img src="foo.jpg">
      for n in src_list[1:]: # [0] is the stuff before the first 'src'
        self.__html_link_count += 1
        end_quote = n.find('"')
        self._Fetch(parent, n[0:end_quote])

  # kml.walk.KMLNodeHandler:HandleNode()
  def HandleNode(self, href, node, llab, lod):
    self.__node_count += 1
    parent = href.Href()
    self._Print('P  ',parent)
    href_nodelist = node.getElementsByTagName('href')
    for href_node in href_nodelist:
      self.__kml_link_count += 1
      child = kml.kmlparse.GetText(href_node)
      self._Fetch(parent, child)
    if self.__check_html:
      self._CheckHtml(parent, node)



def CheckLinks(opts, kmlurl):
  link_checking_node_handler = LinkCheckingNodeHandler(opts)
  hier = kml.walk.KMLHierarchy()
  hier.SetNodeHandler(link_checking_node_handler)
  hier.Walk(kmlurl)
  link_checking_node_handler.PrintSummary()
  return link_checking_node_handler.Status()

