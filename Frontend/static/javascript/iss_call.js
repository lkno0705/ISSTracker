
var bFollowISS = false;
var bFirstLoad = false;
var bDrawISSRoute = false;
var bFirstDraw = false;
var oldLng;
var aIssRouteFirstDraw;
var oldLatLng;
var latlng;
var issIcon;
var issRouteLive;

function ISSCall(){
    var oData = {};
    oData.call = "ISSpos";
    oData.data =  ""
    oData.callback = createISS;
    oData.type = "GET";   
    ajaxCall(oData);
}

function moveISSCall(){
    var oData = {};
    oData.call = "ISSpos";
    oData.data =  ""
    oData.callback = moveISS;
    oData.type = "GET"; 
    ajaxCall(oData);
}

function createISS(oData) {
    // console.log("createISS");     
    var lat = oData.getElementsByTagName("latitude")[0].innerHTML;
    var lon = oData.getElementsByTagName("longitude")[0].innerHTML;

    latlng = L.latLng(lat, lon);
    mymap.flyTo(latlng, 6);
    create([latlng, latlng]);  
    oldLng = lon;
    // console.log("Lang: " + lat + " Long: " + lon);
    // console.log("moveISSbefore");     
    moveISSCall();
}

// function to move the ISS along the Map
function moveISS(oData) {    
    oldLatLng = latlng;    
    var lat = oData.getElementsByTagName("latitude")[0].innerHTML;
    var lon = oData.getElementsByTagName("longitude")[0].innerHTML;
    iss =  {
        "Latitide": lat,
        "Longitude": lon
    };
    if (issIcon){
        var x = parseFloat(oldLng);
        var y = parseFloat(lon);       
        // console.log("Possition difference: " + (x - y) );
        if (parseFloat(oldLng) > parseFloat(lon)) {
            issIcon.removeFrom(mymap);            
            ISSCall();
            if (issRoute)
            {
                issRoute.removeFrom(mymap);
                if (issRouteLive)
                    issRouteLive.removeFrom(mymap);
                callBackEndISSDB();
            }
            return;
        }
        oldLng = lon;
        // console.log("moveISS");
        latlng = L.latLng(lat, lon);
        issIcon.moveTo(latlng, 5000)

        if (bDrawISSRoute && aIssRouteFirstDraw) {
            var aDraw = [];
            if (issRouteLive){
                issRouteLive.remove();
                aDraw = issRouteLive.getLatLngs();
                aDraw.push(latlng);
            }
            if (!bFirstDraw) {
                aDraw.push(aIssRouteFirstDraw);
                aDraw.push(oldLatLng);
                aDraw.push(latlng);
                issRouteLive = L.polyline(aDraw,{
                    className: "gpx",
                }).addTo(mymap);    
                bFirstDraw = true;
            } else {
                issRouteLive = L.polyline(aDraw,{
                    className: "gpx",
                }).addTo(mymap);
            }        
        }

        if (bFollowISS) {
        mymap.panTo(issIcon._latlng,{
            animate: true,
            duration: 5.0,
            easeLinearity: 1
        });   
        mymap.setZoom = 6;          
        }
        issIcon.start();
        // console.log("Lang: " + lat + " Long: " + lon);
        if (!bFirstLoad)
        {
            document.getElementById("loadwrapper").style.display="none";
            changeCursor('default');  
            bFirstLoad= true;
        }
        setTimeout(moveISSCall, 5000);
    }    
}

function followISS(){
    // console.log("followISS");
    if (document.getElementById("followISS").checked)
        {
            // console.log(issIcon);
            mymap.flyTo(latlng,6,{
                duration: 1
            });      
            bFollowISS=true;
            document.getElementById("mapid").style.pointerEvents ="none";
            var kmlLayer = document.getElementsByClassName("leaflet-interactive")
            for (var i = 0; i < kmlLayer.length;i++){
                kmlLayer[i].style.pointerEvents="none";
            }
        }
    else
        {
            bFollowISS=false;
            mymap.setMinZoom(3);
            mymap.setMaxZoom(7);
            document.getElementById("mapid").style['pointer-events'] = "auto";
            var kmlLayer = document.getElementsByClassName("leaflet-interactive")
            for (var i = 0; i < kmlLayer.length;i++){
                kmlLayer[i].style.pointerEvents="";
            }
        }
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