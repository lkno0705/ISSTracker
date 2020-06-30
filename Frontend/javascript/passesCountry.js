// function that handles click on country 
var oneTime = 5;
// var stylesheet = [];

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
        complete: function(oData){countryCallBack(oData);}
    });
}

// creation of html DOM

function countryCallBack(oData){
    var xmlString = "<?xml version='1.0' encoding='UTF-8'?>" +
    "<Request>"+
       "<requestName>ISSCountryPasses</requestName>"+
        "<data>"+
            "<numberOfPasses>4</numberOfPasses>"+
            "<passes>"+
                "<pass>"+
                   "<startTime>2020-06-26 18-15-03</startTime>"+
                    "<endTime>2020-06-26 22-56-39</endTime>"+
                "</pass>" +
            "</passes>"+
        "</data>"+
    "</Request>"
    // var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
    document.getElementById("infoOnCountry").innerHTML='';
    transform2(xmlDoc, 'xsl/countryflyby.xsl', "infoOnCountry")
    // waitForPopUp();
    console.log("PopUp: onCountry"); // XSL transformation
}

// function setDelay(i){
//     setTimeout(countryCallBack);
//     console.log(i);
// }

//setTimeout for PopUp
function waitForPopUp(){
    // setTimeout(countryCallBack, 500);

    // for(var i=0; i <= 5; i++){
    //     setDelay(i);
    // }

    if(oneTime<=4){
        let time = setTimeout(waitForPopUp, 50);
        oneTime += 1;
        // clearTimeout(time);
    }else{
        // clearTimeout(countryCallBack, 50);
        oneTime = 1;
    }
}