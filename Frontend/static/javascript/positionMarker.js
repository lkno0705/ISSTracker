
var radius;
var circle;
var posMarker;

function addMarker(lat,lng,bool){
    if (posMarker)
    posMarker.removeFrom(mymap);
   var latlng = L.latLng(lat, lng);
   posMarker = L.marker(latlng,{draggable:true}).addTo(mymap);
   getFlyByInfo(latlng,bool);
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
    circle.on('mouseover', function(e){
        mymap.scrollWheelZoom.disable();
        window.addEventListener("wheel", mousewheelHandler, true);
    });
    circle.on('mouseout', function(e){
        mymap.scrollWheelZoom.enable();
        window.removeEventListener("wheel", mousewheelHandler, true);    
    });
}

function mousewheelHandler(e) {
    if (e.deltaY)
    {
    var slider = document.getElementById("position_radius");
    var output = document.getElementById("radius");

    if (output.innerHTML >= 0 && output.innerHTML <= 500)
        output.innerHTML = parseInt(output.innerHTML) + parseInt((-e.deltaY/3)*10);

    if (output.innerHTML <= 0)
        output.innerHTML = 10;
        
    if (output.innerHTML >= 500)
        output.innerHTML = 500;

    circle.setRadius( parseInt(output.innerHTML) * 1000);
    slider.value = output.innerHTML;    
    // console.log(e.deltaY);
    }
}
