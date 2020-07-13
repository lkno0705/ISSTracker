// Mag gets created, for options check leaflet docu

var markerLatlng;
var menu;
var menuState;
var active;
var bStart = false;

function createMap() {
    // console.log("create map");
    mymap = L.map('mapid', {
        // continuousWorld:false,
        // worldCopyJump:true,
        maxBoundsViscosity: 1,
        zoomControl: false,
        contextmenu: true,
        contextmenuWidth: 140,
        contextmenuItems: [{
            text: 'show coordinate',
            callback: showCoordinate
        }, {
            text: 'set marker',
            callback: setMarker
        }]
    }).setView([0, 0], 7);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 7,
        minZoom: 3,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery <a href="https://www.mapbox.com/">Mapbox</a>, ' +
            '<a href="impressum.html">Impressum<a> ',
        id: 'mapbox/satellite-streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(mymap);

    L.control.zoom({position: "bottomright"}).addTo(mymap);

    var southWest = L.latLng(-90, -190), northEast = L.latLng(90, 190);
    var bounds = L.latLngBounds(southWest, northEast);

    mymap.setMaxBounds(bounds);

    menu = document.querySelector(".context-menu");
    menuState = 0;
    active = "context-menu--active";

    mymap.on('contextmenu', function (e) {
        removePopUps();
        // console.log(e);    
        markerLatlng = e.latlng;
        toggleMenuOn(e.originalEvent);
    });

    mymap.on('click', function () {
        removePopUps();
    });

    callBackendDrawCounties(mymap);

}

function callBackendDrawCounties(map) {
    var date = new Date();
    $.ajax({
        crossDomain: true,
        type: 'GET',
        url: 'xml/xmlForCounties.xml',
        xml: "application/xml",
        dataType: 'xml',
        success: function (oReturnData) {
            console.log(date.toLocaleTimeString() + " | " + "KML" + " Success!")
            drawCounties(map, oReturnData)
        },
        error: function (oReturnData) {
            console.log(oData.call + ' Failed!');
            console.log(oReturnData)
        }
    });
}

function drawCounties(map, countiesXML) {
    transform3(countiesXML, 'xsl/CountiesXML2KML.xsl', function (oData) {
        // Create new kml overlay
        const parser = new DOMParser();
        const kml = parser.parseFromString(oData,'text/html')
        const track = new L.KML(kml);
        map.addLayer(track);

        // Adjust map to show the kml
        const bounds = track.getBounds();
        map.fitBounds(bounds);
    })


}

function toggleMenuOn(e) {
    if (menuState !== 1) {
        menuState = 1;
        menu.classList.add(active);
        menu.style.left = e.x + "px";
        menu.style.top = e.y + "px";
    } else {
        menuState = 0;
        menu.classList.remove(active);
    }
}

function showCoordinate() {

}

function removePopUps() {
    if (menuState == 1)
        toggleMenuOn();
    document.getElementById("issOnBoard").innerHTML = "";
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
    } else {
        i_text++;
        if (i_text % 2 == 0)
            i_start++;
    }
    setTimeout(loadingText, 20);
}

function changeCursor(cursor) {
    document.body.style.cursor = cursor;
    // document.getElementById("mapid").style.cursor = "none";
}


function getSliderTime() {
    return getCurrentTime(getSliderValue());
}

function getCurrentTime(past) {
    var date = new Date();
    if (past) {
        var time = date.setTime(date.getTime() - past * 60 * 1000);
        date = new Date(time);
    }
    var day = pad(date.getUTCDate(), 2);
    var month = pad(date.getUTCMonth() + 1, 2);
    var year = date.getUTCFullYear();
    var hour = pad(date.getUTCHours(), 2);
    var minute = pad(date.getUTCMinutes(), 2);
    var seconds = pad(date.getUTCSeconds(), 2);

    return "" + year + "-" + month + "-" + day + " " + hour + "-" + minute + "-" + seconds;
}

function pad(n, width, z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function parse2localTime(s) {
    s = s.split(" ")
    date = s[0];
    time = s[1];
    date = date.split("-");
    time = time.split("-");

    var oDate = new Date();
    oDate.setUTCDate(parseInt(date[2]));
    oDate.setUTCMonth(parseInt(date[1] - 1));
    oDate.setUTCFullYear(parseInt(date[0]));
    oDate.setUTCHours(parseInt(time[0]));
    oDate.setUTCMinutes(parseInt(time[1]));
    oDate.setUTCSeconds(parseInt(time[2]));
    test = oDate.toLocaleString();
    return oDate.toLocaleString();
}

$(document).ready(function () {
    // console.log("create map call");   
    changeCursor('wait');
    loadingText(1);
    var mymap;
    createMap();
    ISSCall(createISS);
    getRadiusSliderValue();
    getSliderValue();
    rssCall();
    countriesCallBackEnd();

    $('form input').keydown(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            if (bStart)
                callGeoCoding();
            else
                start();
            return false;
        }
    });
    $(function () {
        var focusedElement;
        $(document).on('focus', 'input', function () {
            if (focusedElement == this) return; //already focused, return so user can now place cursor at specific point in input.
            focusedElement = this;
            setTimeout(function () {
                focusedElement.select();
            }, 100); //select all text in any field on focus for easy re-entry. Delay sightly to allow focus to "stick" before selecting.
        });
    });
});