// Backendcall for RSS-Feed

function rssClick(e){
    callBackEnd(currentTime);
}

function rssCall(){
    callBackEnd(0, 5);
}

function getCurrentTime(){
    var date = new Date();
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();
    var hour = date.getHours();
    var minute  = date.getMinutes();
    var seconds = date.getSeconds();

    return "" + year + "-" + month + "-" + day + " " + hour + "-" + minute + "-" + seconds;
}

function callBackEnd(start, end){
    $.ajax({
        url: 'http://127.0.0.1:8082/RSS-Feed',
        data:"<?xml version='1.0' encoding='UTF-8'?>" +
                "<Request>" +
                    "<requestName>RSS-Feed<requestName>" +
                    "<params>" +
                        "<startID>" + start + "</startID>" +
                        "<endID>" + end + "</endID>" +
                    "</params>" +
                "</Request>",
        type: 'POST',
        crossDomain: true,
        dataType: 'xml',
        success: function() { console.log("Success!")},
        error: function() { console.log('Failed!')},
        complete: function(oData){ RSSCallback(oData);}
    });
}

function RSSCallback(oData){
    var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
    transform2(xmlDoc, 'xsl/rssfeednasa.xsl',"mySidebar"); // XSL transformation
    console.log("RSS-Feed");
    //waitForXSL();
}
