mapboxgl.accessToken = 'pk.eyJ1Ijoic2FtYXJndWxpZXMiLCJhIjoiY2E3c2laTSJ9.v0zuT22Dw8b72E-TRFbFaQ';

// default map settings
var zoom = 13;
var center = [-75.16, 39.95];

var map_settings = document.getElementById('map__container').dataset;

if(map_settings !== null) {
		if( typeof map_settings.zoom !== 'undefined' ) {
		zoom = map_settings.zoom;
	}
	if( typeof map_settings.lat !== 'undefined' && typeof map_settings.lng !== 'undefined' ) {
		center = [map_settings.lat, map_settings.lng];
	}
}
var highlighted_place_id = parseInt(map_settings.placeId);


var map = new mapboxgl.Map({
    container: 'map__container',
    style: 'mapbox://styles/mapbox/light-v9',
	zoom: zoom,
    center: center
});


map.on('load', function() {
	
	map.addSource("places", {
        "type": "vector",
        "tiles": ["http://localhost:8000/places/map/tiles/{z}/{x}/{y}/"],
        "minzoom": 4,
        "maxzoom": 14
	});
	// all places
    map.addLayer({
        "id": "places",
        "type": "circle",
        "source": "places",
        "paint": {
            "circle-color": "hsl(14, 100%, 30%)",
            'circle-radius': {
                "stops": [[8, 2], [12, 6], [22, 12]]
            },            
            "circle-opacity": 0.8
         },
		"filter": ["!=", "id", highlighted_place_id],
        "source-layer": "places"
    });
    map.addLayer({
        "id": "places-label",
        "source": "places",
        "type": "symbol",
        "minzoom": 12,
        "layout": {
            "icon-image": "commercial-15",
            "icon-size": 2,
            "icon-allow-overlap": true,
            "icon-ignore-placement": true,
            "text-field": "{title}",
            "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
            "text-size": 11,
            "text-transform": "uppercase",
            "text-letter-spacing": 0.05,
            "text-offset": [0, 1.75]
        },
        "paint": {
            "text-color": "hsl(14, 100%, 18%)",
            "text-halo-color": "#fff",
            "text-halo-width": 2
        },
		"filter": ["!=", "id", highlighted_place_id],
        "source-layer": "places"
    });
	
	// highlighted place
    map.addLayer({
        "id": "places-highlighted",
        "type": "circle",
        "source": "places",
        "paint": {
            "circle-color": "hsl(14, 100%, 51%)",
            'circle-radius': {
                "stops": [[8, 7], [12, 11], [22, 17]]
            },            
            "circle-opacity": 0.8
         },
		"filter": ["==", "id", highlighted_place_id],
        "source-layer": "places"
    });
    map.addLayer({
        "id": "places-label-highlighted",
        "source": "places",
        "type": "symbol",
        "minzoom": 12,
        "layout": {
            "icon-image": "commercial-15",
            "icon-size": 2,
            "icon-allow-overlap": true,
            "icon-ignore-placement": true,
            "text-field": "{title}",
            "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
            "text-size": 12,
            "text-transform": "uppercase",
            "text-letter-spacing": 0.05,
            "text-offset": [0, 2.25]
        },
        "paint": {
            "text-color": "hsl(14, 100%, 51%)",
            "text-halo-color": "#fff",
            "text-halo-width": 2
        },
		"filter": ["==", "id", highlighted_place_id],
        "source-layer": "places"
    });
    

     // Create a popup, but don't add it to the map yet.
    var popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
    });
    
    map.on('click', 'places', function (e) {
        var id = e.features[0].properties.id;
        window.location = "/places/" + id + "/";
    });

    map.on('mouseenter', 'places', function(e) {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';

        var coordinates = e.features[0].geometry.coordinates.slice();
        var title = e.features[0].properties.title;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup.setLngLat(coordinates)
            .setHTML(title)
            .addTo(map);
    });

    map.on('mouseleave', 'places', function() {
        map.getCanvas().style.cursor = '';
        popup.remove();
    });
    
});