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
        maxZoom: 7,
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
                console.log("PopUp: " + layer.feature.properties.name_sort) 
                //removePopUps();   
                //functins        
            return onCountry(layer.feature.properties.name_sort);//layer.feature.properties.name_sorton.onCountry();
        })//.on('click', onCountry) // should notice an event when clicked
        .addTo(mymap);
        //mainLayer.on("click", onCountry);
    });
}

function showCoordinate(){

}

function removePopUps(){
    if  (menuState == 1)
    toggleMenuOn(); 
    document.getElementById("issOnBoard").innerHTML="";
}

// function drawGeoJSON(){
    // L.geoJSON(json/world_med_res.json, {
    //     style: function (feature) {
    //         return {color: feature.properties.color};
    //     }
    // }).bindPopup(function (layer) {
    //     return layer.feature.properties.description;
    // }).addTo(map);
// }

// test funtion to draw SVG to the map object
// function drawSVG(){
//     var latlngs = [[54.983105,9.921906],  [54.59664,9.93958],  [54.363605,10.950112],  [54.008694,10.939467],  [54.196484,11.956252],  [54.47037,12.51844],  [54.075512,13.647467],  [53.75703,14.119686],  [53.248173,14.353315],  [52.981262,14.074521],  [52.62485,14.4376],  [52.089947,14.685026],  [51.74519,14.607099],  [51.106674,15.016995],  [51.00234,14.570718],  [51.117268,14.3070135],  [50.926918,14.056228],  [50.733234,13.338132],  [50.484077,12.966837],  [50.26634,12.240111],  [49.96912,12.415191],  [49.547417,12.521024],  [49.307068,13.031329],  [48.87717,13.595945],  [48.416115,13.243358],  [48.289146,12.884103],  [47.637585,13.025851],  [47.467644,12.932627],  [47.672386,12.62076],  [47.703083,12.141357],  [47.523766,11.4264145],  [47.5664,10.544504],  [47.302486,10.402083],  [47.580196,9.896069],  [47.52506,9.594226],  [47.830826,8.522612],  [47.61358,8.317302],  [47.620583,7.466759],  [48.33302,7.5936766],  [49.017784,8.099278],  [49.201958,6.65823],  [49.463802,6.1863203],  [49.902225,6.242751],  [50.12805,6.043073],  [50.803722,6.156658],  [51.851616,5.988658],  [51.852028,6.5893965],  [52.22844,6.8428693],  [53.144043,7.0920534],  [53.482162,6.9051394],  [53.69393,7.100425],  [53.748295,7.9362392],  [53.527794,8.121706],  [54.020786,8.8007345],  [54.395645,8.572118],  [54.96274,8.526229],  [54.830864,9.282049],  [54.983105,9.921906]  ];
//     var polygon = L.polygon(latlngs, {color: 'red', id: "germany"}).addTo(mymap);
//     var svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
//     svgElement.setAttribute('xmlns', "http://www.w3.org/2000/svg");
//     svgElement.setAttribute('viewBox', "0 0 100 100");
//     svgElement.innerHTML =  '<polyline points="1188,352 1188,367 1211,376 1211,390 1234,383 1247,372 1273,387 1283,400 1289,419 1282,429 1291,443 1296,463 1294,475 1304,499 1294,502 1288,498 1282,505 1266,512 1257,521 1241,529 1245,539 1247,554 1259,563 1271,578 1263,593 1255,598 1258,620 1256,626 1249,619 1238,618 1222,624 1202,622 1199,631 1187,622 1180,624 1156,613 1151,621 1132,621 1135,596 1146,573 1114,566 1103,557 1104,542 1100,534 1102,510 1098,471 1112,471 1118,457 1123,423 1119,410 1124,402 1143,400 1147,408 1162,389 1157,375 1156,353 1173,358 1188,352 "/>';
//     var svgElementBounds = [ [ 32, -130 ], [ 13, -100 ] ];
//     L.svgOverlay(svgElement, svgElementBounds).addTo(mymap);
// }

//  ISS Icon get initialised
var issPNG = L.icon({
    iconUrl: 'images/issicon_hell.png',   

    iconSize: [100, 100], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

//  function draws ISS icon to map an starts moving it. 
function create(strecke) {
    issIcon = L.Marker.movingMarker(strecke, [100000], { icon: issPNG }).addTo(mymap);
    issIcon.on("click", onBoard);
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

$(document).ready(function () {
    console.log("create map call");
    var mymap;  
    createMap();
    loadingText(1);
    // drawSVG();
    drawGeoJSON();
    coordinate2pixel('xml/germany.xml');
    // renderGPX();
    // addMarker(50.5,30.5);
    getRadiusSliderValue();
    getSliderValue();
    rssCall()
    // callBackEnd();
});