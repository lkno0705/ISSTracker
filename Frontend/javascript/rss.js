// Backendcall for RSS-Feed

var startRss = 0;
var endRss = 5;

function rssClick(e){
    if (e === -1 && startRss !== 0){
        endRss = startRss;
        startRss = startRss - 5;
    }
    else if (e === 1){
        startRss = endRss
        endRss = endRss + 5
    }
    document.getElementById("mySidebar").innerHTML="";
    rssCallBackEnd(startRss, endRss);
}

function rssCall(){
    rssCallBackEnd(0, 5);
}

function rssCallBackEnd(start, end){
    var oData = {};
    oData.call = "RSS-Feed";
    oData.data =        "<Request>" +
                            "<requestName>RSS-Feed<requestName>" +
                            "<params>" +
                                "<startID>" + start + "</startID>" +
                                "<endID>" + end + "</endID>" +
                            "</params>" +
                        "</Request>";
    oData.callback = RSSCallback;
    oData.type = "POST";
    ajaxCall(oData);
}

function RSSCallback(oData){ 
    var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
    if (xmlDoc.childNodes[0].childNodes[1].childNodes.length > 0)
    {
        transform2(xmlDoc, 'xsl/rssfeednasa.xsl',"mySidebar"); // XSL transformation
        console.log("RSS-Feed");       
    }
    else
     rssClick(-1);
}
