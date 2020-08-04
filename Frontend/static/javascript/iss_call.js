"use strict";

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
    var lat = oData.getElementsByTagName("latitude")[0].innerHTML;
    var lon = oData.getElementsByTagName("longitude")[0].innerHTML;

    latlng = L.latLng(lat, lon);
    mymap.flyTo(latlng, 6);
    create([latlng, latlng]);  
    oldLng = lon;    
    moveISSCall();
}

// function to move the ISS along the Map
function moveISS(oData) {    
    oldLatLng = latlng;    
    var lat = oData.getElementsByTagName("latitude")[0].innerHTML;
    var lon = oData.getElementsByTagName("longitude")[0].innerHTML;
    if (issIcon){
        var x = parseFloat(oldLng);
        var y = parseFloat(lon);
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
        // mymap.setZoom = 6;          
        }
        issIcon.start();    
        if (!bFirstLoad)
        {
            var showTutorial = getCookie("tutorial") == "true" ? false : true;
            document.getElementById("startupTutorialCB").checked = !showTutorial;
            if (showTutorial) {
              openModal();
            }
            document.getElementById("loadwrapper").style.display="none";
            document.getElementById("overlay").style.display="none";
            changeCursor('default');  
            bFirstLoad= true;
        }
        setTimeout(moveISSCall, 5000);
    }    
}

function followISS(){    
    if (document.getElementById("followISS").checked) {           
            mymap.flyTo(latlng,6,{
                duration: 1
            });      
            bFollowISS=true;
            document.getElementById("mapid").style.pointerEvents = "none";
            var zoom = document.getElementsByClassName("leaflet-control-zoom");
            for (var i = 0; i < zoom.length;i++){
                zoom[i].style.pointerEvents="none";
            }
            var kmlLayer = document.getElementsByClassName("leaflet-interactive");
            for (var i = 0; i < kmlLayer.length;i++){
                kmlLayer[i].style.pointerEvents="none";
            }
        } else {
            bFollowISS=false;
            document.getElementById("mapid").style['pointer-events'] = "auto";
            var zoom = document.getElementsByClassName("leaflet-control-zoom");
            for (var i = 0; i < zoom.length;i++){
                zoom[i].style.pointerEvents="auto";
            }
            var kmlLayer = document.getElementsByClassName("leaflet-interactive");
            for (var i = 0; i < kmlLayer.length;i++){
                kmlLayer[i].style.pointerEvents="auto";
            }
        }
};

var issPNG = L.icon({
    iconUrl: 'images/International_Space_Station.svg',   
    iconSize: [100, 100], 
    shadowSize: [50, 64], 
    iconAnchor: [0, 0], 
    shadowAnchor: [4, 62],  
    popupAnchor: [-3, -76] 
});

function create(strecke) {
    issIcon = L.Marker.movingMarker(strecke, [100000], { 
        icon: issPNG,
        className: "ISS_icon"
     }).addTo(mymap);
     
    issIcon.on("click", onBoard);
}