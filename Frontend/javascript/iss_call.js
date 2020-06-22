// this function directly calls the ISS-Api, will be refactored to call our own BE
var bFollowISS = false;


function createISS() {
    console.log("createISS");
    $.getJSON('http://api.open-notify.org/iss-now.json?callback=?', function (data) {
        var lat = data['iss_position']['latitude'];
        var lon = data['iss_position']['longitude'];

        var latlng = L.latLng(lat, lon);
        create([latlng, latlng]);
        //marker.setLatLng([lat, lon]);            
        mymap.setView(latlng, 4);

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


var issIcon;
createISS();  