var issRoute;

function renderGPX(oData){
var xmlDoc = oData;
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
      document.getElementById("drawISSroute").disabled=false;     
    }).addTo(mymap);
  })
};

function callBackEndISSDB(){
  var checkbox =  document.getElementById("drawISSroute")
  if (!checkbox.checked) {    
    if (issRoute)
    issRoute.removeFrom(mymap);
  } else {
    checkbox.disabled = true;
    $(".overlay").show();
    $(".loadwrapper").show();
    var x =  getCurrentTime();
    var y = getSliderTime();

    var oData = {};
    
    oData.call = "ISSDB";
    oData.data =        "<requestName>ISSDB</requestName>" + 
                            "<params>" +
                              "<startTime>" + getSliderTime() + "</startTime>"+
                              "<endTime>" + getCurrentTime() + "</endTime>"+
                            "</params>";                        
    oData.callback = renderGPX;
    oData.type = "POST";
    ajaxCall(oData);
  }
};