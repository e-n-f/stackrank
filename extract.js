#!/usr/local/bin/node

"use strict";

var key = require('./key.json');
var turf = require('turf');
var edges = require('./tl_2010_06075_edges.json');

function extract(end, mid, tlid, part, name) {
        // looking from
        var ilon = mid.geometry.coordinates[0];
        var ilat = mid.geometry.coordinates[1];

        // looking toward
        var lon = end.geometry.coordinates[0];
        var lat = end.geometry.coordinates[1];

        var ang = Math.atan2(lat - ilat, lon - ilon) * 180 / Math.PI;

        ang = 360 - ang; // atan2 goes counterclockwise, streetview goes clockwise
        ang += 90;  // atan2 starts at 3:00, streetview starts at 12:00
        ang -= 30;  // look to the left
        ang = ang % 360;

	var ang2 = (ang + 60) % 360; // look to the right

        var url = "http://maps.googleapis.com/maps/api/streetview?size=640x375&key=" + key.key + "&location=" + ilat + "," + ilon + "&fov=60&heading=" + ang + "&pitch=0&sensor=false";
        var url2 = "http://maps.googleapis.com/maps/api/streetview?size=640x375&key=" + key.key + "&location=" + ilat + "," + ilon + "&fov=60&heading=" + ang2 + "&pitch=0&sensor=false";

        console.log(tlid + " " + part + " " + ilat + "," + ilon + " " + lat + "," + lon + " " + ang + " " + url + " " + url2 + " " + name);
}

edges.features.forEach(function(edge) {
        if (! (edge.properties.MTFCC.substring(0, 1) === 'S')) {
                return;
        }

        var len = turf.lineDistance(edge, 'miles');

        if (len < .02) {
                return;
        }

        var end1 = turf.along(edge, 0, 'miles');
        var mid1 = turf.along(edge, .02, 'miles');

        var end2 = turf.along(edge, len, 'miles');
        var mid2 = turf.along(edge, len - .02, 'miles');

        extract(end1, mid1, edge.properties.TLID, "a", edge.properties.FULLNAME);
        extract(end2, mid2, edge.properties.TLID, "b", edge.properties.FULLNAME);
});
