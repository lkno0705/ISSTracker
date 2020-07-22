"use strict";

var bGeoCodingInProgress = false;

function countriesCallBackEnd(){    
        var oData = {};
        oData.call = "CountryList";                    
        oData.callback = countriesCallback;
        oData.type = "GET";
        ajaxCall(oData); 
}

function countriesCallback(oData){     
    transform2(oData, "xsl/countries.xsl", "countries"); // XSLT    
}

function callGeoCoding(){ //parsing of input field
    if (!bGeoCodingInProgress) {
        bGeoCodingInProgress = true;
        var plz = document.getElementById('plz').value;
        var countryName = document.getElementById('country').value;
        var countries = document.getElementsByTagName('option');
        var aCountries =[];
        for (var i = 0 ; i<countries.length;i++){
           aCountries.push(countries[i].value);
        }
        if (aCountries.indexOf(countryName) == -1){
            window.alert("Not a valid country name, please pick a country from the list")
            bGeoCodingInProgress = false;
            return;
        }
        var sParse = addressParser();
        if (sParse)
        {
            if (plz == "" &&  countryName != "" && !bFromMarker){
                geoCodingCallBackEnd(sParse, countryName);
                document.getElementById("flyOver").innerHTML = '<div id=passContainer>' +
                                                               '<p class="text"  id="loadingPasses" style="margin-bottom: -40px;">loading country passes...</p>' +
                                                               '<div id="countrypassesSidebar">' + loadingAnimation + '</div></div>'
            }
            else if(plz != "" && plz.indexOf(",") == -1)
                geoCodingCallBackEnd(sParse);
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
        else {bGeoCodingInProgress = false;}
    }   
}

function addressParser(){
    var zipCode = document.getElementById('plz').value;
    var country = document.getElementById('country').value;
    if (zipCode != "" || country != "")
        return "" + zipCode + ", " + country;
}

function geoCodingCallBackEnd(q, countryName){
    var oData = {};
    oData.e = countryName;
    oData.call = "GeocodingAddress";
    oData.data =        "<requestName>Geocoding</requestName>" +
                            "<params>" +
                            "<q>" + q +"</q>"+
                            "</params>";                        
    oData.callback = geoCodingCallBack;
    oData.type = "POST";
    ajaxCall(oData);
}

function geoCodingCallBack(oData,countryName){ 
    var lat = parseFloat(oData.getElementsByTagName("latitude")[0].innerHTML);
    var lon = parseFloat(oData.getElementsByTagName("longitude")[0].innerHTML);
    var latlng = L.latLng(lat, lon);
    if (countryName == "")
        addMarker(lat,lon);
    else
        onCountry(countryName, true)
    mymap.flyTo(latlng,5);
}