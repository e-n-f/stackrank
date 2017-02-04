#!/usr/local/bin/node

"use strict";

var key = require('./key.json');
var turf = require('turf');
var edges = require('./tl_2010_06075_edges.json');

function extract(end, mid, tlid, part) {
	// looking from
	var ilon = end.geometry.coordinates[0];
	var ilat = end.geometry.coordinates[1];

	// looking toward
	var lon = mid.geometry.coordinates[0];
	var lat = mid.geometry.coordinates[1];

	var ang = Math.atan2(lat - ilat, lon - ilon) * 180 / Math.PI;

        ang = 360 - ang; // atan2 goes counterclockwise, streetview goes clockwise
        ang += 90;  // atan2 starts at 3:00, streetview starts at 12:00
        ang = ang % 360;

	var url = "http://maps.googleapis.com/maps/api/streetview?size=640x640&key=" + key.key + "&location=" + ilat + "," + ilon + "&fov=90&heading=" + ang + "&pitch=0&sensor=false";

	console.log(tlid + " " + part + " " + ilat + "," + ilon + " " + lat + "," + lon + " " + ang + " " + url);
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

	extract(end1, mid1, edge.properties.TLID, "a");
	extract(end2, mid2, edge.properties.TLID, "b");
});
