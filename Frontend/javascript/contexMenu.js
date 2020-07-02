function setMarker(){
    bContextMenu = true;
    console.log("setMarker at: "+ markerLatlng)
    toggleMenuOn();  
    addMarker(markerLatlng.lat,markerLatlng.lng);
}

function getPosition(){
   toggleMenuOn();  
   bContextMenu = true;
   document.getElementById("plz").value = markerLatlng.lat +", "+ markerLatlng.lng;    
}