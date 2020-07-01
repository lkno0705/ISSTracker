// this function directly calls the ISS-Api, will be refactored to call our own BE
var bFollowISS = false;
var oldLng;

function createISS(bReFocus) {
    console.log("createISS");
    $.ajax({
        url: 'http://127.0.0.1:8082/ISSpos',
        data:"",
        type: 'GET',
        crossDomain: true,
        dataType: 'xml',
        // success: function() { console.log("Success!")},
        // error: function() { console.log('Failed!')},
        complete: function(oData){
            var xmlString = oData.responseText;
            var parser = new DOMParser; 
            var xmlDoc = parser.parseFromString(xmlString, "text/xml");
            var lat = xmlDoc.getElementsByTagName("latitude")[0].innerHTML;
            var lon = xmlDoc.getElementsByTagName("longitude")[0].innerHTML;
    
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
        }
      });
    moveISS();
}

// function to move the ISS along the Map
function moveISS() {
    $.ajax({
        url: 'http://127.0.0.1:8082/ISSpos',
        data:"",
        type: 'GET',
        crossDomain: true,
        dataType: 'xml',
        // success: function() { console.log("Success!")},
        // error: function() { console.log('Failed!')},
        complete: function(oData){
            var xmlString = oData.responseText;
            var parser = new DOMParser; 
            var xmlDoc = parser.parseFromString(xmlString, "text/xml");
            var lat = xmlDoc.getElementsByTagName("latitude")[0].innerHTML;
            var lon = xmlDoc.getElementsByTagName("longitude")[0].innerHTML;
        iss =
            {
                "Latitide": lat,
                "Longitude": lon
            };
        var x = parseFloat(oldLng);
        var y = parseFloat(lon);       
        console.log("Possition difference: " + (x - y) );
        if (Math.abs(parseFloat(oldLng) - parseFloat(lon))>1)
        {
         issIcon.removeFrom(mymap);
         createISS(true);
        }
        oldLng = lon;
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
        changeCursor('default');
        issIcon.start();
        console.log("Lang: " + lat + " Long: " + lon);
    }
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
    iconUrl: 'images/International_Space_Station.svg',   
    iconSize: [100, 100], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [0, 0], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});


function create(strecke) {
    issIcon = L.Marker.movingMarker(strecke, [100000], { 
        icon: issPNG,
        className: "ISS_icon"
     }).addTo(mymap);
    issIcon.on("click", onBoard);
    // issIcon.on("mouseover", addBorder);
}


var issIcon;
createISS();  