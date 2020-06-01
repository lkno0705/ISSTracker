function createMap() {
    console.log("create map");
    mymap = L.map('mapid').setView([51.5, -0.09], 5);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/satellite-streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(mymap);
}

var issPNG = L.icon({
    iconUrl: 'images/issicon.png',
    //shadowUrl: 'leaf-shadow.png',

    iconSize: [100, 100], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

function create(strecke) {
    issIcon = L.Marker.movingMarker(strecke, [100000], { icon: issPNG }).addTo(mymap);
    //L.polyline(strecke).addTo(mymap);
    /*
    marker1.once('click', function () {
        marker1.start();
        marker1.closePopup();
        marker1.unbindPopup();
        marker1.on('click', function () {
            if (marker1.isRunning()) {
                marker1.pause();
            } else {
                marker1.start();
            }
        });
        setTimeout(function () {
            marker1.bindPopup('<b>Click me to pause !</b>').openPopup();
        }, 2000);
    })
    */
}

var i_text = 1;
var i_start = 5;
function loadingText() {
    var s = "establishing satelite link...";

    $("#loadingText").text(s.slice(0, i_start + i_text));
    if (i_text == s.length) {
        i_text = 1;
        i_start = 5;
    }
    else {
        i_text++;
        if (i_text % 2 == 0)
            i_start++;
    }
    setTimeout(loadingText, 20);
}

$(document).ready(function () {
    console.log("create map call");
    var mymap;  
    createMap();
    loadingText(1);
});