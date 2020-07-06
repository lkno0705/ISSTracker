function countriesCallBackEnd(){
    var oData = {};
    oData.call = "CountryList";                    
    oData.callback = countriesCallback;
    oData.type = "GET";
    ajaxCall(oData);
}

function countriesCallback(oData){     
    transform2(oData, "xsl/countries.xsl", "countries"); // XSL transformation
    // console.log("country dropdown");   
}

function callGeoCoding(){
    s = document.getElementById('plz').value;
    sParse = addressParser();
    if (sParse)
    {
        if (document.getElementById('plz').value.indexOf(",") == -1 )
            geoCodingCallBackEnd(addressParser());
        else
        {
            var sLatlon = document.getElementById('plz').value;
            sLatlon = sLatlon.split(",");  
            var lat = sLatlon[0];
            var lon = sLatlon[1];
            var lat = parseFloat(lat);
            var lon = parseFloat(lon);
            addMarker(lat,lon,true);
        }
    }
}

function addressParser(){
    var zipCode = document.getElementById('plz').value;
    var country = document.getElementById('country').value;
    if (zipCode != "" || country != "")
        return "" + zipCode + ", " + country;
}

function geoCodingCallBackEnd(q){
    var oData = {};
    oData.call = "GeocodingAddress";
    oData.data =        "<requestName>Geocoding</requestName>" +
                            "<params>" +
                            "<q>" + q +"</q>"+
                            "</params>";                        
    oData.callback = geoCodingCallBack;
    oData.type = "POST";
    ajaxCall(oData);
}

function geoCodingCallBack(oData){
  var xmlDoc = oData;
  var lat = parseFloat(xmlDoc.childNodes[1].childNodes[1].childNodes[0].innerHTML);
  var lon = parseFloat(xmlDoc.childNodes[1].childNodes[1].childNodes[1].innerHTML);
  var latlng = L.latLng(lat, lon);
  addMarker(lat,lon);
  mymap.flyTo(latlng,5);
//   console.log("geoCodingCallBack"); 
}