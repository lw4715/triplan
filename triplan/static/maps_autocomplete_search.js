function initAutocomplete() {
// Create the search box and link it to the UI element.
    var input = document.getElementById('id_location');
    var searchBox = new google.maps.places.SearchBox(input);
    // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 1.3521, lng: 103.8198},
        zoom: 13,
        mapTypeId: 'roadmap'
    });

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function () {
        searchBox.setBounds(map.getBounds());
    });

    var markers = [];

    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', updateMap);

    /* update map when page loads */
    var itemsloaded = google.maps.event.addDomListener(document.body, 'DOMNodeInserted',
        function (e) {
            if (e.target.className === 'pac-item') {
                //remove the listener
                google.maps.event.removeListener(itemsloaded);
                //trigger the events
                google.maps.event.trigger(input, 'keydown', {keyCode: 40})
                google.maps.event.trigger(input, 'keydown', {keyCode: 13})
                google.maps.event.trigger(input, 'focus')
                google.maps.event.trigger(input, 'keydown', {keyCode: 13})
            }
        });

    function updateMap() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach(function (marker) {
            marker.setMap(null);
        });
        markers = [];

        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function (place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }
            var icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
                map: map,
                icon: icon,
                title: place.name,
                position: place.geometry.location
            }));

            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }

            updatePlacesPhoto(place);
        });
        map.fitBounds(bounds);
    };

    function updatePlacesPhoto(place) {
        var photos = place.photos;
        var places_photo = $("#places_photo");
        if (!photos) {
            console.log("No places photos for ", place);
            return;
        }
        var photo_url = photos[0].getUrl({'maxWidth': 600, 'maxHeight': 600});
        places_photo.attr("src", photo_url);
    }
}

