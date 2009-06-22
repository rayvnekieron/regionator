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


# basic regionator tests (no image handling)

./null.py
./print.py
./testcbox.py
./testcoordinates.py
./testregion.py
./testregionator.py
./testkmlregionator.py
./testfeaturequeue.py
./testftor.py
./teststor.py
./testptor.py
./testgenxml.py
./testgenkml.py
./testxml.py
./testkml.py
./testoutline.py
./testmkroot.py

# a box around USA
./boxes.py usboxes 50.0 24.0 -66.0 -125.0 256 2048 4

# ./testpm.py placemarks.kml pmroot.kml pm
./testpm2.py placemarks.kml pm2root.kml pm2

# ./testls.py marin.kml lsroot.kml ls
./testls2.py marin.kml ls2root.kml ls2

./testoutline.py

../scripts/insertregions.py folders.kml folder-regions.kml

./testhierfile.py

./testhref.py

./testgridso.py

./testmodel.py

./testresourcemap.py

./testkmlparse.py

./testkmz.py London_house.kmz lhcopy.kmz

# requires internet capability (does WMS fetches)
./testwms.py

./testwalk.py
./testchecklinks.py
./testmkregionboxes.py
./testcheckregions.py
./testcsvregionator.py
./testicons.py
./testkmlgetopt.py
./testbbox.py
./testphotooverlay.py

# Without the gdal module, do not run these tests
./check-for-gdal.py
gdal_available=$?
if [[ $gdal_available == 0 ]]; then
./testimage.py 
./testcheckimages.py
./testsuperoverlay.py
fi
