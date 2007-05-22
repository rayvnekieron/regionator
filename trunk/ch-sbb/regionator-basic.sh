#!/bin/sh

# Create an RbNL hierachy sorted by importance of the station based
# on the total number of connections with that station.

csvregionator.py ch-stations.csv ch-basic-root.kml ch-basic-dir
