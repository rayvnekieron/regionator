#!/usr/bin/env python

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



# Test printing progress through Regionate'ing showing
# how the Regionator recurses the hierarchy.

import kml.region
import kml.regionhandler
import kml.regionator

class PrintRegionHandler(kml.regionhandler.RegionHandler):

  def Start(self,region):
    print 'Start ====',region.Id(),region.Qid(),region.NSEW()
    depth = region.Depth()
    if depth > 2:
      return [False,False]
    return [True,True]

  def End(self,region):
    print 'End   ====',region.Id(),region.Qid(),region.NSEW()

  def Kml(self,region,kmlfile,kml):
    print 'Kml   ====',region.Id(),region.Qid(),region.NSEW()

myregionator = kml.regionator.Regionator()
myregionator.SetRegionHandler(PrintRegionHandler())
r = kml.region.RootSnap(30,10,40,20)
myregionator.Regionate(r)

qidlist = myregionator.QidList()
for qid in qidlist:
  print qid

