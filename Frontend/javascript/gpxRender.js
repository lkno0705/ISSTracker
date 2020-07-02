var issRoute;

function renderGPX(oData){
var xmlString = oData.responseText;
var parser = new DOMParser; 
var xmlDoc = parser.parseFromString(xmlString, "text/xml");
transform3(xmlDoc, 'xsl/xml2gpx.xsl', function(gpx){
  if (issRoute)
    issRoute.removeFrom(mymap);

  issRoute = new L.GPX(gpx, {
      async: true, 
      marker_options: {
        startIconUrl: '',
        endIconUrl: '',
        shadowUrl: ''
      },    wptIconUrls: '',
        polyline_options: {
          className: "gpx",
          color: 'green',
          opacity: 0.75,
          weight: 3,
          lineCap: 'round'
        }
      }).on('loaded', function(e) {
      mymap.fitBounds(e.target.getBounds());
      $(".overlay").hide();
      $(".loadwrapper").hide();
    }).addTo(mymap);
  })
};

function callBackEndISSDB(){
  var checkbox =  document.getElementById("drawISSroute")
  if (!checkbox.checked) {
    if (issRoute)
    issRoute.removeFrom(mymap);
  } else {
    $(".overlay").show();
    $(".loadwrapper").show();
    var x =  getCurrentTime();
    var y = getSliderTime();
    $.ajax({
      url: 'http://127.0.0.1:8082/ISSDB',
      data: "<?xml version='1.0' encoding='UTF-8'?>" +
      "<Request>" +
      "<requestName>ISSDB<requestName>" + 
      "<params>" +
      "<startTime>" + getSliderTime() + "</startTime>"+
      "<endTime>" + getCurrentTime() + "</endTime>"+
      "</params>" +
      "</Request>",
      type: 'POST',
      crossDomain: true,
      dataType: 'xml',
      success: function() { console.log("Success!")},
      error: function() { console.log('Failed!')},
      complete: function(oData){ renderGPX(oData);}
    });
  }
};