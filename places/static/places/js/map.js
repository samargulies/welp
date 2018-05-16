mapboxgl.accessToken = 'pk.eyJ1Ijoic2FtYXJndWxpZXMiLCJhIjoiY2E3c2laTSJ9.v0zuT22Dw8b72E-TRFbFaQ';

var map = new mapboxgl.Map({
    container: 'map__container',
    style: 'mapbox://styles/mapbox/streets-v9',
	zoom: 13,
    center: [-75.16, 39.95]
});

map.on('load', function() {
	
	map.addSource("places", {
        "type": "vector",
        "tiles": ["http://localhost:8000/places/map/tiles/{z}/{x}/{y}/"],
        "minzoom": 4,
        "maxzoom": 14
	});
    map.addLayer({
        "id": "places",
        "type": "circle",
        "source": "places",
		"paint": {
		    "circle-radius": 10,
		    "circle-color": "rgba(55,148,179,1)",
		},
	    // "layout": {
 // 			"icon-image": "cat",
 // 			"icon-size": 1
 // 		},
        "source-layer": "places"
    });
    // map.addLayer({
//         "id": "places-label",
//         "type": "symbol",
//         "source": "places",
// 	    "layout": {
// 			"text-field": "{title}",
// 			"text-font": [
// 				"DIN Offc Pro Medium",
// 				"Arial Unicode MS Bold"
// 			],
// 			"text-size": 12
// 		},
//         "source-layer": "places"
//     });
});