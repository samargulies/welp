window.onload = function(){
	document.body.classList.add('js');
}

if( document.querySelector('.place-detail__images--extended') !== null ) {
	var flkty = new Flickity( '.place-detail__images--extended', {
		cellAlign: "left",
		pageDots: false,
		fullscreen: true,
		imagesLoaded: true,
		setGallerySize: false,
		percentPosition: true,
		lazyLoad: 2,
		on: {
			staticClick: function( event, pointer, cellElement, cellIndex ) {
			  // dismiss if cell was not clicked
			    if ( !cellElement ) {
			      return;
			    }

			    flkty.select(cellIndex);
				flkty.toggleFullscreen();
				flkty.reposition()
			}
		}
	});
}

if( document.getElementById('map__container') !== null ) {

	mapboxgl.accessToken = 'pk.eyJ1Ijoic2FtYXJndWxpZXMiLCJhIjoiY2E3c2laTSJ9.v0zuT22Dw8b72E-TRFbFaQ';

	// default map settings
	var zoom = 13;
	var center = [-75.16, 39.95];

	var map_settings = document.getElementById('map__container').dataset;

	if(map_settings !== null) {
			if( typeof map_settings.zoom !== 'undefined' && map_settings.zoom !== '' ) {
			zoom = map_settings.zoom;
		}
		if( typeof map_settings.lat !== 'undefined' && typeof map_settings.lng !== 'undefined'
		 	&& map_settings.lat !== '' && map_settings.lng !== '' ) {
			center = [map_settings.lat, map_settings.lng];
		}
	}
	var highlighted_place_id = parseInt(map_settings.placeId);

	var highlight_filter = ["==", "id", highlighted_place_id];
	var highlight_remove_filter = ["!=", "id", highlighted_place_id];

	if( typeof map_settings.buildingId !== 'undefined' && map_settings.buildingId !== '' ) {
		var highlighted_building_id = parseInt(map_settings.buildingId);
		highlight_filter = ["==", "building_id", highlighted_building_id];
		highlight_remove_filter = ["!=", "building_id", highlighted_building_id];
	}
	
	console.log(highlight_filter);
	
	var map = new mapboxgl.Map({
	    container: 'map__container',
	    style: 'mapbox://styles/mapbox/light-v9',
		zoom: zoom,
	    center: center
	});


	map.on('load', function() {

		map.addSource("places", {
	        "type": "vector",
	        "tiles": [document.location.origin + "/places/map/tiles/{z}/{x}/{y}/"],
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
			"filter": highlight_remove_filter,
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
			"filter": highlight_remove_filter,
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
			"filter": highlight_filter,
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
			"filter": highlight_filter,
	        "source-layer": "places"
	    });


	     // Create a popup, but don't add it to the map yet.
	    var popup = new mapboxgl.Popup({
	        closeButton: false,
	        closeOnClick: false
	    });

	    map.on('click', 'places', function (e) {
	        window.location.href = e.features[0].properties.url;
	        return false;
	    });

	    map.on('mouseenter', 'places', function(e) {
	        // Change the cursor style as a UI indicator.
	        map.getCanvas().style.cursor = 'pointer';

	        var coordinates = e.features[0].geometry.coordinates.slice();
	        var html = "<div class='map-popup'><h3 class='map-popup__title'>" + e.features[0].properties.title + "</h3>";
			if( typeof e.features[0].properties.address !== "undefined" ) {
		        html += "<p class='map-popup__address'>" + e.features[0].properties.address + "</p>";
			}
			if( typeof e.features[0].properties.image !== "undefined" ) {
		        html += "<img class='map-popup__image' src='" + e.features[0].properties.image + "' />";
			}
			html += "</div>";

	        // Ensure that if the map is zoomed out such that multiple
	        // copies of the feature are visible, the popup appears
	        // over the copy being pointed to.
	        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
	            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
	        }

	        // Populate the popup and set its coordinates
	        // based on the feature found.
	        popup.setLngLat(coordinates)
	            .setHTML(html)
	            .addTo(map);
	    });

	    map.on('mouseleave', 'places', function() {
	        map.getCanvas().style.cursor = '';
	        popup.remove();
	    });

	});
}

var simplemde;

if( document.getElementById('add-comment__text-editor') !== null ) {

	simplemde = new SimpleMDE({
		element: document.getElementById("add-comment__text-editor"),
		toolbar: ["bold", "italic", "|", "link", "|", "unordered-list", "ordered-list", "|", "quote", "preview", "guide"],
		status: false,
		spellChecker: false
	});

	simplemde.codemirror.options.extraKeys['Tab'] = false;
	simplemde.codemirror.options.extraKeys['Shift-Tab'] = false;

}

function commentSubmit(e) {
	console.log(e);
	document.getElementById('add-comment__text-editor').value = simplemde.value();
};

var form = document.getElementById('add-comment__form');

if( form !== null ) {
	form.addEventListener('submit', commentSubmit);
	document.querySelector('.add-comment__field__submit').addEventListener('click', commentSubmit);
}

function onloadRecaptcha() {
	var recaptcha = document.getElementById('g-recaptcha-response');
	if( recaptcha !== null ) {
		recaptcha.setAttribute("required", "required");
	}
}


