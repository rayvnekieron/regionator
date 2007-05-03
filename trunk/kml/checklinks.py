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


class LinkCheckingNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self, opts):
    self.__check_kml = False
    self.__check_html = False
    self.__check_absolute = False
    self.__check_relative = False
    self.__verbose = False
    self.__summary = False
    self.__md5 = None
    self.__encoding = None

    opts, args = getopt.getopt(opts, "khravsce:")
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
        self.__summary = True
      elif o == '-s':
        self.__summary = True
      elif o == '-c':
        self.__md5 = md5.new('')
      elif o == '-e':
        self.__encoding = a

    self.__node_count = 0
    self.__kml_link_count = 0
    self.__html_link_count = 0
    self.__relative_link_count = 0
    self.__absolute_link_count = 0
    self.__hostname_only_link_count = 0
    self.__empty_link_count = 0

    self.__max_file_size = 0
    self.__max_file_url = None
    self.__min_file_size = sys.maxint
    self.__min_file_url = None
    self.__size_count = 0
    self.__total_size = 0

    self.__error_count = 0

  def GetEncoding(self):
    return self.__encoding

  def Status(self):
    return self.__error_count

  def Statistics(self):
    return (self.__node_count,
            self.__kml_link_count,
            self.__html_link_count,
            self.__relative_link_count,
            self.__absolute_link_count,
            self.__hostname_only_link_count,
            self.__empty_link_count,
            self.__error_count,
            self.Checksum())

  def Checksum(self):
    if self.__md5:
      return self.__md5.hexdigest()
    return None

  def PrintSummary(self):
    if not self.__summary:
      return
    self.__verbose = True # yuck
    self._Print('X  ', '%d nodes' % self.__node_count)
    if self.__check_kml:
      self._Print('X  ','%d kml links' % self.__kml_link_count)
    if self.__check_html:
      self._Print('X  ','%d html links' % self.__html_link_count)
    if self.__check_relative:
      self._Print('X  ','%d relative links' % self.__relative_link_count)
    if self.__check_absolute:
      self._Print('X  ','%d absolute links' % self.__absolute_link_count)
    self._Print('X  ','%d hostname links' % self.__hostname_only_link_count)
    self._Print('X  ','%d empty links' % self.__empty_link_count)
    self._Print('X  ', '%d max' % self.__max_file_size)
    self._Print('X  ', self.__max_file_url)
    self._Print('X  ', '%d min' % self.__min_file_size)
    self._Print('X  ', self.__min_file_url)
    self._Print('X  ', '%d total' % self.__total_size)
    if self.__size_count:
      self._Print('X  ', '%d count' % self.__size_count)
      ave = self.__total_size/self.__size_count
    else:
      ave = -1
    self._Print('X  ', '%d average' % ave)

    self._Print('X  ','%d errors' % self.__error_count)
    sum = self.Checksum()
    if sum:
      self._Print('X  ','%s checksum' % sum)

  def _Print(self, code, data, *more):
    if self.__verbose:
      print code,data,
      for m in more:
        print m,
      print # newline

  def _SaveSize(self, size, url):
    self.__size_count += 1
    if size > self.__max_file_size:
      self.__max_file_size = size
      self.__max_file_url = url
    if size < self.__min_file_size:
      self.__min_file_size = size
      self.__min_file_url = url
    self.__total_size += size

  def _Fetch(self, parent, child):
    # Handle empty href and count this separately from errors.
    if not child:
      self._Print('EMP','[empty]',parent)
      self.__empty_link_count += 1
      return

    if kml.href.IsRoot(child):
      return # Don't fetch root:// icons

    # href's are often just a hostname (www.foo.com).  This converts
    # these to an absolute URL.  We still print the original href contents.
    prchild = child
    if kml.href.IsHostname(child):
      # Make child an absolute URL to pass the next test more nicely
      child = 'http://' + child
      self._Print('HST',prchild,child)
      self.__hostname_only_link_count += 1

    # Count and fetch only if asked to.
    if kml.href.IsRelative(child):
      if not self.__check_relative:
        return
      self.__relative_link_count += 1
    else:
      if not self.__check_absolute:
        return
      self.__absolute_link_count += 1

    # Print only if asked to count this type of link.
    self._Print('C  ',prchild)

    # Compute the absolute URL and try to fetch it.
    url = kml.href.ComputeChildUrl(parent, child)
    self._Print('U  ',url)

    # If url is a foo.kmz/bar.ext fetch foo.kmz
    (url, file_path) = kml.href.SplitKmzPath(url)
    data = kml.href.FetchUrl(url)
    if data:
      numbytes = len(data)
      self._SaveSize(numbytes, url)
      self._Print('D  ', numbytes)
      if self.__md5:
        self.__md5.update(data)
    else:
      self._Print('ERR',child,parent)
      self.__error_count += 1
    

  def _CheckHtml(self, parent, node):
    links = kml.walk.GetHtmlLinksInNode(node)
    self.__html_link_count += len(links)
    for link in links:
      self._Fetch(parent, link)

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
  encoding = link_checking_node_handler.GetEncoding()
  if encoding:
    hier.SetEncoding(encoding)
  if not hier.Walk(kmlurl):
    return -1 # kmlurl non-existent or failed parse
  link_checking_node_handler.PrintSummary()
  return link_checking_node_handler.Status()

