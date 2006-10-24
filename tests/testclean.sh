#!/bin/sh

# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# $URL$
# $Revision$
# $Date$


# clean up after tests.sh and testimg.sh

rm -f testkml.kml
rm -f testxml.xml
rm -f root.kml
rm -f ancestors.kml
rm -rf usboxes
rm -rf pmroot.kml pm
rm -rf lsroot.kml ls
rm -f outline.kml
rm -f folder-regions.kml
rm -f screeno.kml screeno*.jpg
rm -f gridso.kml gridso*.jpg
rm -rf mv-polys
rm -f terra.kml terra_e.jpg terra_w.jpg
rm -rf llb-0.kml llb-0
rm -rf llb-d.kml llb-d
rm -rf llb-a.kml llb-a
rm -rf llb-t.kml llb-t
rm -rf llb-3.kml llb-3
rm -f lhcopy.kmz
