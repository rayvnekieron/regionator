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
import os
import sys
import time
import kml.walk
import kml.href
import kml.kmlgetopt


class LinkCheckingNodeHandler(kml.walk.KMLNodeHandler):

  def __init__(self, go):
    self.__check_kml = go.Get('k')
    self.__check_html = go.Get('h')
    self.__check_absolute = go.Get('a')
    self.__check_relative = go.Get('r')
    self.__verbose = go.Get('v')
    self.__summary = go.Get('s')
    if go.Get('c'):
      self.__md5 = md5.new('')
    else:
      self.__md5 = None
    self.__nofetch = go.Get('n')

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
    self.__total_bytes = 0
    self.__total_seconds = 0

    self.__error_count = 0

    self.__start_time = time.time()

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
    self._Print('X  ', '%d total bytes' % self.__total_bytes)
    if self.__size_count:
      self._Print('X  ', '%d files' % self.__size_count)
      ave = self.__total_bytes/self.__size_count
      self._Print('X  ', '%d average bytes/file' % ave)
    if self.__total_bytes and self.__total_seconds:
      bps = (self.__total_bytes * 8) / self.__total_seconds
      self._Print('X  ', '%s average bps' % kml.href.PrettyBPS(bps))
      overall_seconds = time.time() - self.__start_time
      self._Print('X  ', '%d seconds overall' % overall_seconds)
      bps = (self.__total_bytes * 8) / overall_seconds
      self._Print('X  ', '%s overall bps' % kml.href.PrettyBPS(bps))

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

  def _SaveSizeAndTime(self, bytes, url, seconds):
    self.__size_count += 1
    if bytes > self.__max_file_size:
      self.__max_file_size = bytes
      self.__max_file_url = url
    if bytes < self.__min_file_size:
      self.__min_file_size = bytes
      self.__min_file_url = url
    self.__total_bytes += bytes
    self.__total_seconds += seconds

  def Fetch(self, parent, child):
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

    # "checklinks.py -n ..."
    if self.__nofetch:
      return

    fetcher = kml.href.Fetcher(url)
    # If url is a foo.kmz/bar.ext this fetches foo.kmz
    data = fetcher.FetchData()
    if data:
      numbytes = fetcher.Size()
      self._SaveSizeAndTime(numbytes, url, fetcher.Time())
      self._Print('D  ', numbytes)
      self._Print('T  ', fetcher.PrettyBPS())
      if self.__md5:
        self.__md5.update(data)
    else:
      self._Print('ERR',child,parent)
      self.__error_count += 1
    
  def FetchHtmlLinks(self, parent, links):
    self.__html_link_count += len(links)
    for link in links:
      self.Fetch(parent, link)

  def _CheckHtml(self, parent, node):
    links = kml.walk.GetHtmlLinksInNode(node)
    self.FetchHtmlLinks(parent, links)

  # kml.walk.KMLNodeHandler:HandleNode()
  def HandleNode(self, href, node, llab, lod):
    self.__node_count += 1
    parent = href.Href()
    self._Print('P  ',parent)
    href_nodelist = node.getElementsByTagName('href')
    for href_node in href_nodelist:
      self.__kml_link_count += 1
      child = kml.kmlparse.GetText(href_node)
      self.Fetch(parent, child)
    if self.__check_html:
      self._CheckHtml(parent, node)


def ParseArgv(argv):
  return kml.kmlgetopt.Getopt(argv, 'kharvsce:u:n')

def CheckKmlLinks(go):
  link_checking_node_handler = LinkCheckingNodeHandler(go)
  hier = kml.walk.KMLHierarchy()
  hier.SetNodeHandler(link_checking_node_handler)
  encoding = go.Get('e')
  if encoding:
    hier.SetEncoding(encoding)
  if not hier.Walk(go.Get('u')):
    return -1 # kmlurl non-existent or failed parse
  link_checking_node_handler.PrintSummary()
  return link_checking_node_handler.Status()

def CheckLinks(argv):
  go = ParseArgv(argv)
  kmlurl = go.Get('u')
  if not kmlurl:
    return -1
  return CheckKmlLinks(go)

def CheckCsvLinks(argv):
  """Check HTML links in CSV file
  Checks all unique links in <a href=""> and <img src=""> in
  the last field of each line in the CSV file.
  Args:
    -a: fetch absolute links
    -r: fetch relative links
    -v: verbose output
    -s: compute a checksum of fetched links
    -s: print summary
  Returns:
    status: count of link fetch failures
  """
  go = ParseArgv(argv)
  csvfile = go.Get('u')
  file = kml.href.OpenFileForRead(csvfile)
  if not file:
    return -1
  parent_dir = os.path.dirname(csvfile)
  
  # Gather all the links
  link_list = []
  for csv_line in file:
    tuple = csv_line.split('|')
    last_item = tuple[-1]
    kml.walk.GetLinksInHtml(last_item, link_list)

  # Cull duplicates
  link_map = {}
  for link in link_list:
    link_map[link] = 1

  # Fetch each unique link
  link_checking_node_handler = LinkCheckingNodeHandler(go)
  link_checking_node_handler.FetchHtmlLinks(parent_dir, link_map.keys())

  # Report status
  link_checking_node_handler.PrintSummary()
  return link_checking_node_handler.Status()

