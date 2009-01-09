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



import kml.genkml

_kml = []
_kml.append(kml.genkml.KML21())
_kml.append('<Document>\n')

_kml.append('\n')
name = '1'
href = 'screeno01.jpg'
draworder = 0
x = 0
y = 0
wid = 64
ht = 64
_kml.append(kml.genkml.ScreenOverlay(name, href, draworder, x, y, wid, ht))

_kml.append('\n')
name = '2'
href = 'screeno02.jpg'
draworder = 0
x = 64
y = 64
wid = 64
ht = 64
_kml.append(kml.genkml.ScreenOverlay(name, href, draworder, x, y, wid, ht))

_kml.append('\n')
name = '3'
href = 'screeno03.jpg'
draworder = 1
x = 0
y = 0
wid = 32
ht = 32
_kml.append(kml.genkml.ScreenOverlay(name, href, draworder, x, y, wid, ht))

_kml.append('\n')
name = '4'
href = 'screeno04.jpg'
draworder = 1
x = 32
y = 32
wid = 32
ht = 32
_kml.append(kml.genkml.ScreenOverlay(name, href, draworder, x, y, wid, ht))


_kml.append('\n')
_kml.append('</Document>\n')
_kml.append('</kml>')

f = open('screeno.kml','w')
f.write("".join(_kml))
f.close()

