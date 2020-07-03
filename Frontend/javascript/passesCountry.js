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
    var oData = {};
    
    oData.call = "ISSCountryPasses";
    oData.data =        "<Request>" +
                          "<requestName>ISSCountryPasses<requestName>" + 
                            "<params>" +
                            "<startTime>" + getCurrentTime(720) +"</startTime>" +
                            "<endTime>" + getCurrentTime() +"</endTime>" +
                            "<country>" + countryName + "</country>" +
                            "</params>" +
                          "</Request>",
    oData.callback = countryCallBack;
    oData.type = "POST";
    ajaxCall(oData);
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