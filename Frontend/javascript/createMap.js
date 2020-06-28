// Mag gets created, for options check leaflet docu

var markerLatlng;
var menu;
var menuState;
var active;

function createMap() {
    console.log("create map");
    mymap = L.map('mapid',{
        // continuousWorld:false,
        worldCopyJump:true,
        maxBoundsViscosity: 1,
        zoomControl:false,
        contextmenu:true,
        contextmenuWidth: 140,
        contextmenuItems:[{
            text: 'show coordinate',
            callback: showCoordinate
        },{
            text: 'set marker',
            callback: setMarker
        }]
    }).setView([51.5, -0.09], 5);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 13,
        minZoom: 2,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/satellite-streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(mymap); 
    
    L.control.zoom({position:"bottomright"}).addTo(mymap);

    var southWest = L.latLng(-90, -190), northEast = L.latLng(90, 190);
    var bounds = L.latLngBounds(southWest, northEast);
    
    mymap.setMaxBounds(bounds);

    menu = document.querySelector(".context-menu");
    menuState = 0;
    active = "context-menu--active";

    mymap.on('contextmenu', function(e) {
        removePopUps();
        console.log(e);    
        markerLatlng = e.latlng;
        toggleMenuOn(e.originalEvent);    
      });
    
    mymap.on('click', function() {
        removePopUps(); 
      });

      
   
}

function toggleMenuOn(e) {
    if ( menuState !== 1 ) {
    menuState = 1;
    menu.classList.add(active);
    menu.style.left = e.x+"px";
    menu.style.top = e.y+"px";
    }
    else{
        menuState = 0;
        menu.classList.remove(active);
    }
}

// trying to clone the geoJSON layers to add the copies to the neighboring maps; result: the user should be able to click on neighbouring maps

var mainLayer;

// funtion to draw geoJson to map, just for test purposes 
function drawGeoJSON(){
    $.getJSON("json/world_med_res.json", function(json) {
        data = json;
        console.log(json); // this will show the info it in firebug console
        mainLayer=L.geoJSON(json, {
                style: function (feature) {
                    return {color: '#FFFFFF',
                            opacity: .2,
                            fillOpacity: 0};
                }
            }).bindPopup(function (layer) {  
                removePopUps();   
                //functins        
            return layer.feature.properties.name_sort;
        })//**.bindTooltip('click for more information')
        .addTo(mymap);
    });
}

function showCoordinate(){

}

function removePopUps(){
    if  (menuState == 1)
    toggleMenuOn(); 
    document.getElementById("issOnBoard").innerHTML="";
    bCrewPopUp = false;
}

var i_text = 1;
var i_start = 5;
// loading text animation, can be scapped, when loading times improve. 
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

function getSliderTime(){    
  return  getCurrentTime( getSliderValue());
}

function getCurrentTime(past){
 

    var date = new Date(); 
    if (past) {
        var time = date.setTime( date.getTime() - past*60*1000);
        date = new Date(time);
    }
    var day = pad(date.getUTCDate(),2);
    var month = pad(date.getUTCMonth() + 1,2);
    var year = date.getUTCFullYear();
    var hour = pad(date.getUTCHours(),2);
    var minute  = pad(date.getUTCMinutes(),2);
    var seconds = pad(date.getUTCSeconds(),2);

    return "" + year + "-" + month + "-" + day + " " + hour + "-" + minute + "-" + seconds;
}

function pad(n, width, z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
  }

$(document).ready(function () {
    console.log("create map call");
    var mymap;  
    createMap();
    loadingText(1);
    // drawSVG();
    drawGeoJSON();
    coordinate2pixel('xml/germany.xml');
    // renderGPX();
    // callBackEndISSDB();
    // addMarker(50.5,30.5);
    getRadiusSliderValue();
    getSliderValue();
    rssCall()
    // callBackEnd();
});