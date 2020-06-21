var radius;
var circle;
function addMarker(lat,lng){
   var latlng = L.latLng(lat, lng);
   posMarker = L.marker(latlng,{draggable:true}).addTo(mymap);
   addCircle(latlng,radius);
   posMarker.on('drag', function(e){
    var chagedPos = e.target.getLatLng();
    addCircle(chagedPos);
   });
}

function addCircle(latlng){
    if (circle)
     circle.removeFrom(mymap);
    var slider = document.getElementById("position_radius");
    circle = L.circle(latlng, slider.value*1000).addTo(mymap);
}