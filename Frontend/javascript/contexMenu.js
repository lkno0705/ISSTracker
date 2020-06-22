function setMarker(){
    console.log("setMarker at: "+ markerLatlng)
    toggleMenuOn();  
    addMarker(markerLatlng.lat,markerLatlng.lng);
}

function getPosition(){
   toggleMenuOn();  
   document.getElementById("plz").value = markerLatlng.lat +", "+ markerLatlng.lng;    
}