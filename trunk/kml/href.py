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

"""

Utility class to create and parse URLs
for use with KML <href>

"""

import urlparse
import urllib2
import os.path
import copy
import tempfile
import socket

class Href:

  def __init__(self):
    #self.__scheme = 'http'
    self.__scheme = None
    self.__netloc = None
    # path = dirname / basename
    self.__dirname = None
    self.__basename = None
    self.__querylist = []
    self.__fragment = None

  def GetScheme(self):
    return self.__scheme

  def SetScheme(self, scheme):
    self.__scheme = scheme

  def SetHostname(self, hostname):
    self.__netloc = hostname

  def SetPath(self, path):
    # XXX non-unix systems?
    # borrowing os.path for url's is improper...
    (dirname,basename) = os.path.split(path)
    self.__dirname = dirname
    self.__basename = basename

  def SetBasename(self, basename):
    self.__basename = basename

  def SetDirname(self, dirname):
    self.__dirname = dirname

  def SetUrl(self, url):
    (scheme, netloc, path, query, fragment) = urlparse.urlsplit(url)
    if len(scheme):
      self.__scheme = scheme
    if len(netloc):
      self.__netloc = netloc
    self.SetPath(path)

  def AddQuery(self, query):
    self.__querylist.append(query)

  def AddQueryNameValue(self, name, value):
    self.AddQuery('%s=%s' % (name, value))

  def Query(self):
    return "&amp;".join(self.__querylist)

  def Path(self):
    if self.__dirname and self.__dirname != '/':
      return self.__dirname + '/' + self.__basename
    else:
      return self.__basename

  def Href(self):

    """ URL string appropriate for KML <href>

    """

    arg = []
    arg.append(self.__scheme)
    arg.append(self.__netloc)
    """
    # This is URL so raw '/' is okay
    if self.__dirname and self.__dirname != '/':
      path = self.__dirname + '/' + self.__basename
    else:
      path = self.__basename
    arg.append(os.path.normpath(path))
    """
    arg.append(os.path.normpath(self.Path()))
    arg.append(self.Query())
    arg.append(self.__fragment)
    return urlparse.urlunsplit(arg)


def FetchUrl(url):
  if IsHttp(url):
    txdata = None
    txheaders = {   
      'User-Agent': 'regionator',
      'Accept': '*/*',
    }
    req = urllib2.Request(url, txdata, txheaders)
    try:
      f = urllib2.urlopen(req)
    except:
      return None
  else:
    try:
      f = open(url,'r')
    except:
      return None
  return f.read()


def FetchUrlToTempFile(url):
  (fd, name) = tempfile.mkstemp()
  data = FetchUrl(url)
  if data:
    os.write(fd, data)
  else:
    name = None
  os.close(fd)
  return name
  

def SplitKmzPath(href_text):
  dot_kmz_slash = href_text.find('.kmz/')
  if dot_kmz_slash == -1:
    return (href_text, None)

  split_pos = dot_kmz_slash + 4 # '.kmz/'
  kmz_path = href_text[:split_pos]
  file_path = href_text[split_pos+1:]
  return (kmz_path, file_path)


def SplitKmzHref(parent_href, href_text):

  """ Split out the parts of a path pointing into a .kmz

  Args:
    parent_href: kml.href.Href() of kml file with the given href_text
    href_text: a path string typically straight out of <Link><href>

  Returns:
    (kmz_path, file_path):
                 kmz_path: filename/url of .kmz file
                file_path: filename inside the .kmz (.zip) archive
  """
  (kmz_path, file_path) = SplitKmzPath(href_text)
  if kmz_path:
    kmz_href = copy.deepcopy(parent_href)
    kmz_href.SetBasename(kmz_path)
    return (kmz_href.Href(), file_path)
  return (parent_href.Href(), file_path)


def IsHttp(url):
  return url[:7] == 'http://'

def IsRoot(url):
  return url[:7] == 'root://'

def IsRelative(url):
  href = Href()
  href.SetUrl(url)
  path = href.Path()
  if not path:
    return False
  return href.GetScheme() == None and path[0] != '/'

def IsHostname(hostname):
  # Anything with a space is not a hostname
  if hostname.find(' ') != -1:
    return False
  # Anything with no dot near the end is not a hostname
  dot = hostname.rfind('.')
  if len(hostname) - dot > 4:
    return False
  # Any blah.tld that has an ipaddr is definitely a hostname
  try:
    ipaddr = socket.gethostbyname(hostname)
    return True
  except:
    return False


def ComputeChildUrl(parent_href, child_href):

  """Compute the URL to the child relative to the parent

  Possibilities for either href and the return include:
    - absolute http   http://foo.com/goo.kml
    - relative        dir/goo.kml
    - a kmz           dir/foo.kmz
    - inside a kmz    http://foo.com/goo.kmz/bar.kml

  Args:
    parent_href: the parent.kml 
    child_href: the contents of an <href> inside the parent.kml

  Returns:
    url: absolute URL to the child

  """

  # If the child is absolute we're done
  if IsHttp(child_href) or IsRoot(child_href):
    return child_href

  # See if the parent is KMZ
  (url, file) = SplitKmzPath(parent_href)

  if url and not file:
    # Parent is ...parent.kml
    href = Href()
    href.SetUrl(parent_href)
    href.SetBasename(child_href)
    return href.Href()
