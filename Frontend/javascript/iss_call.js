// this function directly calls the ISS-Api, will be refactored to call our own BE
var bFollowISS = false;
var oldLng;

function createISS(bReFocus) {
    console.log("createISS");
    $.getJSON('http://api.open-notify.org/iss-now.json?callback=?', function (data) {
        var lat = data['iss_position']['latitude'];
        var lon = data['iss_position']['longitude'];

        var latlng = L.latLng(lat, lon);
        create([latlng, latlng]);
        //marker.setLatLng([lat, lon]); 
        if (!bReFocus) 
        {   
        console.log("refocus");
        mymap.setView(latlng, 4);
        }
        oldLng = lon;
        console.log("Lang: " + lat + " Long: " + lon);
        console.log("moveISSbefore");
        // setTimeout(moveISS(), 5000);
    });
    setTimeout(moveISS, 5000);
}

// function to move the ISS along the Map
function moveISS() {
    $.getJSON('http://api.open-notify.org/iss-now.json?callback=?', function (data) {
        var lat = data['iss_position']['latitude'];
        var lon = data['iss_position']['longitude'];
        iss =
            {
                "Latitide": lat,
                "Longitude": lon
            };
        var x = parseFloat(oldLng);
        var y = parseFloat(lon);       
        console.log("Possition difference: " +(x-y) );

        if (Math.abs(parseFloat(oldLng) - parseFloat(lon))>1)
        {
         issIcon.removeFrom(mymap);
         createISS(true);
        }

        oldLng = lon;
        //marker.setLatLng([lat, lon]);
        //mymap.setView(marker.getLatLng(), mymap.getZoom()); 
        console.log("moveISS");
        latlng = L.latLng(lat, lon);
        issIcon.moveTo(latlng, 5000)
        if (bFollowISS)
        {
            mymap.panTo(latlng);
            mymap.setZoom(5);
        }
        $(".overlay").hide();
        $(".loadwrapper").hide();
        issIcon.start();
        console.log("Lang: " + lat + " Long: " + lon);
        //latlng1 = L.latLng(lat, lon);
        // moveISS();
    });

    setTimeout(moveISS, 5000);
}

function drawISS(){
    console.log("drawRoute");
}

function followISS(){
console.log("followISS");
if (document.getElementById("followISS").checked)
    bFollowISS=true;
else
    bFollowISS=false;
};

var issPNG = L.icon({
    iconUrl: 'images/issicon_hell.png',   

    iconSize: [100, 100], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});


function create(strecke) {
    issIcon = L.Marker.movingMarker(strecke, [100000], { icon: issPNG }).addTo(mymap);
    issIcon.on("click", onBoard);
}


var issIcon;
createISS();  