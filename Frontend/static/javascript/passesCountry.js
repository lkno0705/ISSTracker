"use strict";

// function that handles click on country 
var setCountryPopUp = false;
var country;
var routePopup = document.getElementsByClassName('leaflet-popup-pane')
function onCountry(countryName, destination){    
    toggleLoading(false,!destination,true);
    country = countryName;
    changeCursor('wait');
    if(!setCountryPopUp){
    removePopUps();
    setCountryPopUp = true; 
    callCountryBackEnd(countryName, destination);
    }
}

// call to Backend for info
function callCountryBackEnd(countryName, destination){    
    var oData = {};
    oData.e = {'destination': destination,
               'countryName': countryName
            };
    oData.call = "ISSCountryPasses";
    oData.data =        "<requestName>ISSCountryPasses</requestName>" + 
                            "<params>" +
                            "<startTime>" + getCurrentTime(720) +"</startTime>" +
                            "<endTime>" + getCurrentTime() +"</endTime>" +
                            "<country>" + countryName + "</country>" +
                            "</params>";                        
    oData.callback = countryCallBack;
    oData.type = "POST";
    ajaxCall(oData);
}

// creation of html DOM
function countryCallBack(oData, e){
    var xmlDoc = oData;
    routePopup[0].style.display = 'block';
    var startTimes = oData.getElementsByTagName("startTime");
    var endTimes = oData.getElementsByTagName("endTime");
    if( startTimes.length){
        for (var i = 0; i < startTimes.length; i++)
        {
            if(startTimes[i].innerHTML != "")
                startTimes[i].innerHTML = parse2localTime(startTimes[i].innerHTML);
            if(endTimes[i].innerHTML != "")
                endTimes[i].innerHTML = parse2localTime(endTimes[i].innerHTML);
        }
    }
    if (!e.destination){
        document.getElementById("countryPasses").innerHTML = "";
        transform2(xmlDoc, 'xsl/countryflyby.xsl', "countryPasses");
    } else {
        document.getElementById("passContainer").innerHTML = '<div id="countrypassesSidebar"><div id="countryHeader"></div><div id="countryContent"></div></div>';
        document.getElementById("countryHeader").innerHTML = "<h2>Flyby over " + e.countryName + "</h2>";
        transform2(xmlDoc, 'xsl/countryflyby_sidebar.xsl', "countryContent");
    }


    toggleLoading(true);
    setCountryPopUp = false;
    bGeoCodingInProgress = false;
}