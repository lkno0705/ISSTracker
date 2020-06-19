function renderGPX(){
var gpx = 'gpx/run.gpx'; // URL to your GPX file or the GPX itself
new L.GPX(gpx, {async: true, 
    polyline_options: {
      color: 'green',
      opacity: 0.75,
      weight: 3,
      lineCap: 'round'
    } }).on('loaded', function(e) {
  mymap.fitBounds(e.target.getBounds());
}).addTo(mymap);

// var worldGGPX = 'gpx/world_med_res.gpx'; // URL to your GPX file or the GPX itself
// new L.GPX(worldGGPX, {async: true, 
//     polyline_options: {
//       color: 'green',
//       opacity: 0.75,
//       weight: 3,
//       lineCap: 'round'
//     } }).on('loaded', function(e) {
//   mymap.fitBounds(e.target.getBounds());
// }).addTo(mymap);
}