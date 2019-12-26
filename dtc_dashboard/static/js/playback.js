iconsmap = {}
function returnicon(iconnumber) {
    var busurl = "/static/bus_icon/" + iconnumber + ".png";
    return new L.Icon({
        iconUrl: busurl,
        iconSize: [30, 45],
        iconAnchor: [12, 45],
        popupAnchor: [1, -34],
        shadowSize: [45, 45]
    })
}
function getnewicon(vehicle_id) {
    if (typeof getnewicon.counter == 'undefined') {
        getnewicon.counter = 0;
    }
    if (vehicle_id in iconsmap) {

    }
    else {
        iconsmap[vehicle_id] = returnicon(getnewicon.counter % 13);
        getnewicon.counter++;
    }

    return iconsmap[vehicle_id];
}
function map_points(map, options) {
    map.removeControl(map.zoomControl);
    var zoomHome = L.Control.zoomHome({ position: 'topleft' });
    zoomHome.addTo(map);
    var heading = document.getElementById("p1");
    var timeelapsed = 0;



    $("#playbackcheck").click(function (event) {
        // alert("You changed the button using JQuery!" + $(this).val());
        if ($("#vehicle_id_field").val() == -1) {
            alert('Reselect Vehicle Id');
        }
        else {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', filtered_routes, true);
            xhr.onreadystatechange = xhrCallback;
            xhr.send();
            function xhrCallback() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText);
                    const trackplayback = L.trackplayback(data, map, {
                        clockOptions: {
                            speed: 5,
                            maxSpeed: 65
                        },
                        targetOptions: {
                            useImg: false,
                            width: 12,
                            height: 27,
                            color: '#0066cc',
                            fillColor: '#0066cc',
                            // imgUrl: "{% static 'bus_icon/ship.png' %}"
                        }
                    });
                    const trackplaybackControl = L.trackplaybackcontrol(trackplayback);
                    trackplaybackControl.addTo(map);
                }
            }
        }
    });
}
