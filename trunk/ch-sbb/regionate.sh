#!/bin/sh
./cleanup.sh
./regionator-basic.sh
ln -s balloon.kml style/style.kml
./regionator-style.sh
./regionator-multi.py
