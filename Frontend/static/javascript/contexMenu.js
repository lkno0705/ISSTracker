"use strict";

// functions of the context menu

// context menu
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

function setMarker(){
    bContextMenu = true; 
    toggleMenuOn();  
    addMarker(markerLatlng.lat,markerLatlng.lng); // set marker
}

function getPosition(){
   toggleMenuOn();  
   bContextMenu = true;
   document.getElementById("plz").value = markerLatlng.lat +", "+ markerLatlng.lng;  // writes coordinates to search bar  
}

//dummy function
function showCoordinate() {

}