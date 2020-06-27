// function that handles click on country 
function onCountry(countryName){
    removePopUps();
    callCountryBackEnd(countryName);
}

// call to Backend for info

function callCountryBackEnd(countryName){
    $.ajax({
        url: 'http://127.0.0.1:8082/ISSCountryPasses',
        data:"<?xml version='1.0' encoding='UTF-8'?>" +
       "<Request>" +
            "<requestName>ISSDB<requestName>" +
            "<params>" + 
                    "<startTime>2019-06-15 12-00-00</startTime>" +
                    "<endTime>" + getCurrentTime() +"</endTime>" +
                    "<country>" + countryName + "</country>" +
            "</params>" +
        "</Request>",
        type: 'POST',
        crossDomain: true,
        dataType: 'xml',
        success: function() { console.log("Success!")},
        error: function() { console.log('Failed!')},
        complete: function(oData){ countryCallBack(oData);}
    });
}

// creation of html DOM

function countryCallBack(oData){
    var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
    transform2(xmlDoc, 'xsl/countryflyby.xsl',"infoOnCountry"); // XSL transformation
    console.log("PassBy");
   // document.getElementById("infoOnCountry").style.left=e.originalEvent.x + "px";
   // document.getElementById("infoOnCountry").style.top=e.originalEvent.y + "px"; 
    console.log("onCountry");
    //waitForXSL();
}

function waitForXSL(){
    var slides = document.getElementsByClassName("mySlides");
    if (slides.length!=0) 
    showSlides(1);
  
    setTimeout(waitForXSL, 50);
  } 