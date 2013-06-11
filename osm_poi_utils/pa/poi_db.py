#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

from lxml import etree


############################################################
#
#
############################################################

class POIDb(object):

    def __init__(self):
        self._db = {}

    def get_pois_in_lon_lat_box(self, lon1, lat1, lon2, lat2):
        ### print lon1, lat1, lon2, lat2  
        ### print self._db 
        ret_j = []
        for k,j in self._db.iteritems():
            ### print j  
            if ( j.get('lon') <= max(lon1,lon2) and j.get('lon') >= min(lon1,lon2) ) and ( j.get('lat') <= max(lat1,lat2) and j.get('lat') >= min(lat1,lat2) ):
                ret_j.append(j)
        #
        return ret_j



############################################################
#
#
############################################################

class OSM_POIDb(POIDb):

    def __init__(self):
        self._db = {}


    def make_fromOSMXml(self, fname):
        r = etree.parse(fname)
        for n in r.iter("node"):
            ln, lt = (n.get("lon", 0), n.get("lat", 0))
            j = { "lon": float(ln), "lat": float(lt), }
            t_kv = {}
            for kvn in n.iter("tag"): t_kv[kvn.get("k","k")] = kvn.get("v",'')
            for a in [("addr:city", 'unknown'), ("cuisine",'unknown'), ("amenity", 'unknown'), ("name", 'unknown')]:
                j[a[0]] = t_kv.get(a[0], a[1])
            #
            ### print j 
            self._db[ '_'.join([str(j.get("lon")), str(j.get("lat")), j.get("name")]) ] = j 
            #
        #
                


if "__main__" == __name__ :
    pdb = OSM_POIDb()
    pdb.make_fromOSMXml("bar.sfbayarea.xml")
    pdb.make_fromOSMXml("restaurant.sfbayarea.xml")

