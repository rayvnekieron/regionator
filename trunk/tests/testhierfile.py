#!/usr/bin/python

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

import kml.hierfile

hf3 = kml.hierfile.HierFile(3)

flatname = 'abcdefgh'
(dir,name) = hf3.HierName(flatname)
print 'HierFile 3',flatname,dir,name
if dir != 'abc/def/' or name != 'gh':
  print 'ERROR: HierFile failed'

flatname = '0123456789abcdefghijklmnopqrstuvwzyz'
(dir,name) = hf3.HierName(flatname)
print 'HierFile 3',flatname,dir,name

hf6 = kml.hierfile.HierFile(6)
(dir,name) = hf6 = hf6.HierName(flatname)

path = hf3.Path('foobar')
if path != 'foo/bar':
  print 'ERROR: HierFile Path() failed'
print 'HierFile.Path()',path
