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

    } else {
        iconsmap[vehicle_id] = returnicon(getnewicon.counter % 13);
        getnewicon.counter++;
    }

    return iconsmap[vehicle_id];
}

function getbusstops() {
    var stops_var = new L.GeoJSON.AJAX(all_stops, {
        pointToLayer: function(feature, latlng) {
            return L.marker(latlng, {
                icon: new L.Icon({
                    iconUrl: staticpath+'bus_icon/stop.png',
                    iconSize: [15, 22],
                    iconAnchor: [6, 22],
                    popupAnchor: [1, -34],
                    shadowSize: [22, 22]
                }),
                title: feature.properties.stop_name,
                riseOnHover: true
            });
        },
        onEachFeature: function(feature, layer) {
            // layer.bindPopup(feature.properties.stop_name.toString());
            layer.bindPopup("Stop Name: " + feature.properties.stop_name.toString() +
                "<br>" + "Stop Code: " + feature.properties.stop_code.toString() +
                "<br>" + "Stop Id: " + feature.properties.stop_id.toString()
            );
        }
    });
    return stops_var;
}

var stops_points = getbusstops();

function returnfilterbuses() {
    return new L.GeoJSON.AJAX(filtered_buses, {
        pointToLayer: function(feature, latlng) {
            return L.marker(latlng, {
                icon: getnewicon(feature.properties.vehicle_id),
                title: feature.properties.vehicle_id,
                riseOnHover: true
            });
        },
        onEachFeature: function(feature, layer) {
            layer.bindPopup("Bus Number: " + feature.properties.vehicle_id.toString() +
                "<br>" + "Speed: " + feature.properties.speed.toString() +
                "<br>" + "Route id: " + feature.properties.route_id.toString()
            );
        }
    });
}
function colorcongestion(congestionlevel)
{
    if(congestionlevel == 0)
    {
        return 'green';
    }
    else if(congestionlevel == 1)
    {
        return 'orange';
    }
    return 'red';
}
function map_init(map, options) {
    map.removeControl(map.zoomControl);
    var zoomHome = L.Control.zoomHome({
        position: 'topleft'
    });
    zoomHome.addTo(map);
    var markers = L.markerClusterGroup({chunkedLoading: true});
    map.addLayer(markers);
    var datapoints = returnfilterbuses();
    datapoints.addTo(map);

    var controlLayers = map.layerscontrol;

    controlLayers.addOverlay(stops_points, "Bus Stops");

    L.control.liveupdate({
            update_map: function() {
                
                if($("#vehicle_id_field_live").val() != -1)
                {
                    datapoints.refresh(filtered_buses);
                    console.log($("#vehicle_id_field_live").val());
                    $.ajax({
                            url:polylineurl,
                            type: 'get',
                            success: function(resp)
                            {
                                    console.log(resp);
                                    console.log(resp[0]);
                                    new L.Polyline([
                                    [resp[0]['latitude'],resp[0]['longitude']],
                                    [resp[1]['latitude'],resp[1]['longitude']]
                                    ], {
                                    color: colorcongestion(resp[0]['congestion']),
                                    weight: 5,
                                    opacity: 0.5
                                    }).addTo(map);

                            }
                        });



                }
                else
                { 
                    urll = all_buses;
$.ajax({
    url:urll,
    type: 'get',
     success: function(resp)
     {
         var geoJsonLayer = L.geoJson(resp, {
            pointToLayer: function(feature, latlng) {
            return L.marker(latlng, {
                icon: getnewicon(feature.properties.vehicle_id),
                title: feature.properties.vehicle_id,
                riseOnHover: true
            });
        },
    onEachFeature: function (feature, layer) {
        
        layer.bindPopup("Bus Number: " + feature.properties.vehicle_id.toString() +
                "<br>" + "Speed: " + feature.properties.speed.toString() +
                "<br>" + "Route id: " + feature.properties.route_id.toString());
    }
});
markers.clearLayers();
markers.addLayers(geoJsonLayer);
     }
});
}/////end of all_buses

},
            position: 'topleft',
            interval: 9000
        })
        .addTo(map)
        .startUpdating();
        var current_position, current_accuracy;

function onLocationFound(e) {
if (current_position) {
  map.removeLayer(current_position);
  map.removeLayer(current_accuracy);
}

var radius = e.accuracy / 2;

current_position = L.marker(e.latlng).addTo(map)
.bindPopup("You are within " + radius + " meters from this point").openPopup();

current_accuracy = L.circle(e.latlng, radius).addTo(map);
}

function onLocationError(e) {
alert(e.message);
}

map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);

// wrap map.locate in a function    
function locate() {
map.locate({setView: true, maxZoom: 16});
}

// call locate every 3 seconds... forever
// setInterval(locate, 3000);
}