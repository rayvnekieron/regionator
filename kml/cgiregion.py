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

Utility functions for Region-based CGI scripting.

A common Region query string is passed down to "child" CGI:

  REGION=qid,n,s,e,w (%d,%f,%f,%f,%f)

"""

import kml.region
import kml.genkml

regkey='REGION'

# create the Region Query String
def CreateQuery(region):
  (n,s,e,w) = region.NSEW()
  region = '%s=%s,%f,%f,%f,%f' % (regkey,region.Qid(),n,s,e,w)
  return region

def GetHref(baseurl,region):
  query = CreateQuery(region)
  href = '%s?%s' % (baseurl,query)
  return href

# parse out the Region Query String
# fs = cgi.FieldStorage()
def Parse(fs):
  if fs.has_key(regkey):
    regval = fs[regkey].value
    reglist = regval.split(',')
    if reglist.__len__() == 5:
      qid = reglist[0]
      n = float(reglist[1])
      s = float(reglist[2])
      e = float(reglist[3])
      w = float(reglist[4])
      r = kml.region.Region(n,s,e,w,qid)
      return r
  # no valid REGION= found
  return 0


def LinkChild(baseurl,pregion,q,minpx,maxpx):
  cregion = pregion.Child(q)
  # Describe the child region cgi and kml
  href = GetHref(baseurl,cregion)
  (n,s,e,w) = cregion.NSEW()
  qid = cregion.Qid()
  return kml.genkml.RegionNetworkLink(n,s,e,w,qid,href,minpx,maxpx)


def GetChildren(region):
  if region.Depth() < 24: # XXX
    return ['0','1','2','3']
  return []

