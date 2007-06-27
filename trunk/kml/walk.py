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

import os
import tarfile
import xml.dom.minidom
import kml.genkml
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
    self.__walk_style_urls = False

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

  def SetWalkStyleUrls(self, bool):
    self.__walk_style_urls = bool

  def _WalkStyleUrls(self, kmlfile, doc):
    styleurl_map = {}
    styleurl_nodelist = doc.getElementsByTagName('styleUrl')
    if styleurl_nodelist:
      for styleurl_node in styleurl_nodelist:
        (url, id) = kml.kmlparse.ParseStyleUrl(styleurl_node)
        if url:
          if styleurl_map.has_key(url):
             styleurl_map[url] += 1
          else:
             styleurl_map[url] = 1
     
      for styleurl in styleurl_map.keys():
        child_url = kml.href.ComputeChildUrl(kmlfile, styleurl)
        self.Walk(child_url, None, None)

  def _WalkNetworkLinks(self, kmlfile, doc, maxdepth):
    networklink_nodelist = doc.getElementsByTagName('NetworkLink')
    for networklink_node in networklink_nodelist:
      (llab,lod) = kml.kmlparse.ParseFeatureRegion(networklink_node)
      child_href = kml.kmlparse.GetNetworkLinkHref(networklink_node)
      child_url = kml.href.ComputeChildUrl(kmlfile, child_href)
      self.Walk(child_url, llab, lod, maxdepth)

  def Walk(self, kmlfile, llab=None, lod=None, maxdepth=-1):
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
    if maxdepth == 0:
      return True
    if maxdepth == -1:
      nmaxdepth = -1
    else:
      nmaxdepth = maxdepth - 1

    if self.__verbose:
      print kmlfile

    href = kml.href.Href()
    href.SetUrl(kmlfile)
    if os.path.isdir(kmlfile):
      kmldata = GetNetworkLinksFromTree(kmlfile)
    elif os.path.isfile(kmlfile) and kmlfile.endswith('.tgz'):
      kmldata = GetNetworkLinksFromTar(kmlfile, self.__encoding)
    else:
      kmldata = kml.href.FetchUrl(href.Href())
    
    doc = kml.kmlparse.ParseStringUsingCodec(kmldata, self.__encoding)
    if not doc:
      if self.__verbose:
        print kmlfile,'load or parse error'
      return False

    if not self.__node_handler:
      return False

    self.__node_handler.HandleNode(href, doc, llab, lod)

    self._WalkNetworkLinks(kmlfile, doc, nmaxdepth)

    if self.__walk_style_urls:
      self._WalkStyleUrls(kmlfile, doc)

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
  

def GetNetworkLinksFromTree(dir):
  """ Create a Folder of NetworkLinks to .kml/.kmz files in dir
  Each NetworkLink/Link/href will be dir/file.km[lz]
  Args:
    dir: dirname
  Returns:
    kml: '<Folder><NetworkLink>...</NetworkLink>...</Folder>'
  """
  folder = kml.genxml.Folder()
  for root,dirs,files in os.walk(dir):
    for file in files:
      if file.endswith('.kmz') or file.endswith('.kml'):
        # XXX on windows each \ in file must be changed to /
        href = '%s/%s' % (root,file)
        folder.Add_Feature(kml.genkml.NetworkLink(href))
  return folder.xml()


def GetNetworkLinksFromTar(tarfilepath, encoding):
  """ Create a Folder of NetworkLinks in KML in the tarfile """
  folder = kml.genxml.Folder()
  folder.name = tarfilepath
  tf = tarfile.open(tarfilepath)
  for ti in tf:
    if ti.isfile():
      name = ti.name
      # TODO: KMZ: extract kml file
      if name.endswith('.kml'):
        flo = tf.extractfile(ti)
        doc = kml.kmlparse.ParseStringUsingCodec(flo.read(), 'latin1')
        sub_folder = kml.genxml.Folder()
        sub_folder.name = name
        networklink_nodelist = doc.getElementsByTagName('NetworkLink')
        for networklink_node in networklink_nodelist:
          child_href = kml.kmlparse.GetNetworkLinkHref(networklink_node)
          sub_folder.Add_Feature(kml.genkml.NetworkLink(child_href))
        folder.Add_Feature(sub_folder.xml())
  return folder.xml()

