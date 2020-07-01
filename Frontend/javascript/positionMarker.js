var radius;
var circle;
var posMarker;
function addMarker(lat,lng){
    if (posMarker)
    posMarker.removeFrom(mymap);
   var latlng = L.latLng(lat, lng);
   posMarker = L.marker(latlng,{draggable:true}).addTo(mymap);
   getFlyByInfo(latlng);
   addCircle(latlng,radius);
   posMarker.on('drag', function(e){
    bContextMenu = true;
    var chagedPos = e.target.getLatLng();
    addCircle(chagedPos);
   });
   posMarker.on('moveend', function(e){
    bContextMenu = true;   
    getFlyByInfo(e.target._latlng);
   })
}

function addCircle(latlng){
    if (circle)
     circle.removeFrom(mymap);
    var slider = document.getElementById("position_radius");
    circle = L.circle(latlng, slider.value*1000,{
        className: "circle"
    }).addTo(mymap);
}

