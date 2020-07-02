function countriesCallBackEnd(){
    $.ajax({
        url: 'http://127.0.0.1:8082/GeoJson',
        data: "<?xml version='1.0' encoding='UTF-8'?>"+
        "<Request>"+
        "<requestName>GeoJson<requestName>"+
        "<params>"+
        "<country>all</country>"+
        "</params>"+
        "</Request>",
        type: 'POST',
        crossDomain: true,
        dataType: 'xml',
        success: function() { console.log("Success!")},
        error: function() { console.log('Failed!')},
        complete: function(oData){ countriesCallback(oData);}
    });
}

function countriesCallback(oData){
    var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
    transform2(xmlDoc, 'xsl/countries.xsl',"countries"); // XSL transformation
    console.log("country dropdown");
    //waitForXSL();
}

function callGeoCoding(){
    s = document.getElementById('plz').value;

    if (document.getElementById('plz').value.indexOf(",") < 0)
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



function addressParser(){
    var zipCode = document.getElementById('plz').value;
    var country = document.getElementById('country').value;
    return "" + zipCode + ", " + country;
}

function geoCodingCallBackEnd(q){
    $.ajax({
        url: 'http://127.0.0.1:8082/GeocodingAddress',
        data: "<?xml version='1.0' encoding='UTF-8'?>"+
        "<Request>"+
        "<requestName>Geocoding<requestName>"+
        "<params>"+
        "<q>" + q +"</q>"+
        "</params>"+
        "</Request>",
        type: 'POST',
        crossDomain: true,
        dataType: 'xml',
        success: function() { console.log("GeocodingAddress Success!")},
        error: function() { console.log('GeocodingAddress Failed!')},
        complete: function(oData){ geoCodingCallBack(oData);}
    });
}

function geoCodingCallBack(oData){
  var xmlString = oData.responseText;
  var parser = new DOMParser; 
  var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
  var lat = parseFloat(xmlDoc.childNodes[0].childNodes[1].childNodes[0].innerHTML);
  var lon = parseFloat(xmlDoc.childNodes[0].childNodes[1].childNodes[1].innerHTML);
  var latlng = L.latLng(lat, lon);
  addMarker(lat,lon);
  mymap.flyTo(latlng,5);
  console.log("geoCodingCallBack"); 
}