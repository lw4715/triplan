$(document).ready(function() {
    $("#map-zoom").click(function () {
        $("#default-map").toggleClass("hide");
        $("#zoomed-map").toggleClass("hide");
        console.log("zooming");
    });

    $("#fav").on('click', function () {
        $.ajax({
            url: 'fav/',
            data: {itinerary_id: $(this).attr('data-itinerary-id')},
            type: 'POST',
            csrfmiddlewaretoken: "{{ csrf_token }}"
        })
    });
});
