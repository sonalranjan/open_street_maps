#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from lxml import etree
import json

import geopy
import geopy.distance

from pyproj import Geod
from impermium.geotztools.distance import Distance  # MaxMind based tools - from Impermium libraries

from pa.poi_db import OSM_POIDb


############################################################
# Wrappers for GEO queries
#
############################################################
class MeetingPlaceAroundGeo(object):

    def __init__(self, debug=2):
        self._debug = debug
        self._dist_obj = Distance()
        self._geod = Geod(ellps='WGS84')
        ############################################################
        # POI-DB
        ############################################################
        opdb = OSM_POIDb()
        opdb.make_fromOSMXml("bar.sfbayarea.xml")
        opdb.make_fromOSMXml("restaurant.sfbayarea.xml")
        opdb.make_fromOSMXml("cafe.sfbayarea.xml")
        self._opdb = opdb

    def get_lon_lat_box(self, lon, lat, radius=10, in_miles=False):
        distance_in_metres = radius*1000
        if in_miles: distance_in_metres = distance_in_metres*1.60934
        nesw_ll = self._geod.fwd([lon]*4, [lat]*4, [0,90,180,270], [distance_in_metres]*4)
        ### print nesw_ll 
        return ( (min(nesw_ll[0]), max(nesw_ll[0])), (min(nesw_ll[1]), max(nesw_ll[1])) )


    def get_amenities_around_city(self, city, country='us', region=None, radius=10, in_miles=False):
        bb_arr = self._dist_obj.get_city_lon_lat(city, country, region)
        ### print dll_arr 
        xbb_arr = [ self.get_lon_lat_box(t[0], t[1], radius, in_miles) for t in bb_arr]
        #
        #
        for bb in xbb_arr:
            if self._debug >= 2: print "Bounding box: ", bb
            a = self._opdb.get_pois_in_lon_lat_box(bb[0][0], bb[1][0], bb[0][1], bb[1][1])
            yield a




if "__main__" == __name__ :

    ############################################################
    # Geo Queries and Utils
    ############################################################
    m = MeetingPlaceAroundGeo(debug=2)
    for c in sys.stdin:
        q = json.loads(c.strip())
        print "*"*80
        print "Query params: ", q
        print "*"*80
        for result_jsons in m.get_amenities_around_city(**q):
            for j in result_jsons:
                print j.get("lon"), j.get("lat"), json.dumps(j)
        print "*"*80
