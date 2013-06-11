#!/usr/bin/env bash


for v_amenity in "bar" "bbq" "cafe" "fast_food" "restaurant"; do

    q_string="http://www.overpass-api.de/api/xapi?node[amenity=${v_amenity}][bbox=-122.99702,36.49012,-120.4372,38.34847]"
    f_string="${v_amenity}.sfbayarea.xml"
    curl --location --globoff ${q_string} -o ${f_string}

done

