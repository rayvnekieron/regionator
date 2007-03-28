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
import kml.superoverlay


class ImageCheckingNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self, opts):
    self.__check_absolute = False
    self.__check_relative = False
    self.__verbose = False

    opts, args = getopt.getopt(opts, "khrav")
    for o,a in opts:
      if o == '-r':
        self.__check_relative = True
      elif o == '-a':
        self.__check_absolute = True
      elif o == '-v':
        self.__verbose = True

    self.__node_count = 0
    self.__image_count = 0
    self.__max_image_size = 0
    self.__max_image_url = None
    self.__min_image_size = 200000000 # XXX maxint
    self.__min_image_url = None
    self.__total_size = 0

  def Status(self):
    return 0

  def Statistics(self):
    return (self.__max_image_size, self.__max_image_url,
            self.__min_image_size, self.__min_image_url,
            self.__image_count, self.__total_size)

  def _RecordStatistics(self, size, url):
    self.__image_count += 1
    if size > self.__max_image_size:
      self.__max_image_size = size
      self.__max_image_url = url
    if size < self.__min_image_size:
      self.__min_image_size = size
      self.__min_image_url = url
    self.__total_size += size

  def PrintSummary(self):
    self._Print('X  ', '%d nodes' % self.__node_count)
    self._Print('X  ', '%d images' % self.__image_count)
    self._Print('X  ', '%d max' % self.__max_image_size)
    self._Print('X  ', self.__max_image_url)
    self._Print('X  ', '%d min' % self.__min_image_size)
    self._Print('X  ', self.__min_image_url)
    self._Print('X  ', '%d total' % self.__total_size)
    if self.__image_count:
      ave = self.__total_size/self.__image_count
    else:
      ave = -1
    self._Print('X  ', '%d average' % ave)

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
      self.empty_link_count += 1
      return

    # Count and fetch only if asked to.
    if kml.href.IsRelative(child):
      if not self.__check_relative:
        return
    else:
      if not self.__check_absolute:
        return

    # Be verbose only if asked and only about links we're asked to check.
    if self.__verbose:
      self._Print('C  ',child)

    # Compute the absolute URL and try to fetch it.
    url = kml.href.ComputeChildUrl(parent, child)
    self._Print('U  ',url)
    data = kml.href.FetchUrl(url)
    if data:
      self._Print('D  ',len(data))
      self._RecordStatistics(len(data), url)
    else:
      self._Print('ERR',child,parent)
      self.__error_count += 1


  # kml.walk.KMLNodeHandler:HandleNode()
  def HandleNode(self, href, node, llab, lod):
    self.__node_count += 1
    parent = href.Href()
    self._Print('P  ',parent)
    for icon_node in node.getElementsByTagName('Icon'):
      href_nodelist = icon_node.getElementsByTagName('href')
      for href_node in href_nodelist:
        self._Fetch(parent, kml.kmlparse.GetText(href_node))


def CheckImages(opts, kmlurl):
  image_checking_node_handler = kml.checkimages.ImageCheckingNodeHandler(opts)
  hier = kml.walk.KMLHierarchy()
  hier.SetNodeHandler(image_checking_node_handler)
  hier.Walk(kmlurl)
  image_checking_node_handler.PrintSummary()
  return image_checking_node_handler.Status()

