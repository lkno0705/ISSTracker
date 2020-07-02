// function that handles click on country 
var setCountryPopUp = false;
var country;
function onCountry(countryName){
    country = countryName;
    changeCursor('wait');
    if(!setCountryPopUp){
    removePopUps();
    setCountryPopUp = true; 
    callCountryBackEnd(countryName);
    }
}

// call to Backend for info
function callCountryBackEnd(countryName){    
    $.ajax({
        url: 'http://127.0.0.1:8082/ISSCountryPasses',
        data:"<?xml version='1.0' encoding='UTF-8'?>" +
       "<Request>" +
            "<requestName>ISSDB<requestName>" +
            "<params>" + 
                    "<startTime>" + getCurrentTime(720) +"</startTime>" +
                    "<endTime>" + getCurrentTime() +"</endTime>" +
                    "<country>" + countryName + "</country>" +
            "</params>" +
        "</Request>",
        type: 'POST',
        crossDomain: true,
        dataType: 'xml',
        success: function() { console.log("Success!")},
        error: function() { console.log('Failed!')},
        complete: function(oData){countryCallBack(oData, countryName);}
    });
}

// creation of html DOM
function countryCallBack(oData, countryName){
    var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
if( xmlDoc.childNodes[0].childNodes[1].childNodes[1].childNodes.length){
    for (var i = 0; i < xmlDoc.childNodes[0].childNodes[1].childNodes[1].childNodes.length; i++)
    {
       if(xmlDoc.childNodes[0].childNodes[1].childNodes[1].childNodes[i].childNodes[0].innerHTML != "")
        xmlDoc.childNodes[0].childNodes[1].childNodes[1].childNodes[i].childNodes[0].innerHTML = parse2localTime(xmlDoc.childNodes[0].childNodes[1].childNodes[1].childNodes[i].childNodes[0].innerHTML);
      if(xmlDoc.childNodes[0].childNodes[1].childNodes[1].childNodes[i].childNodes[1].innerHTML != "")
        xmlDoc.childNodes[0].childNodes[1].childNodes[1].childNodes[i].childNodes[1].innerHTML = parse2localTime(xmlDoc.childNodes[0].childNodes[1].childNodes[1].childNodes[i].childNodes[1].innerHTML);
    }
}
    document.getElementById("countryPasses").innerHTML = "";
    transform2(xmlDoc, 'xsl/countryflyby.xsl', "countryPasses");
    console.log("PopUp: onCountry");
    changeCursor('default');
    setCountryPopUp = false;
}