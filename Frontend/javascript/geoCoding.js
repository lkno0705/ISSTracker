function countriesCallBackEnd(){
    $.ajax({
        url: 'http://127.0.0.1:8082/GeoJson',
        data: "<?xml version='1.0' encoding='UTF-8'?>"+
        "<Request>"+
        "<requestName>ISSDB<requestName>"+
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