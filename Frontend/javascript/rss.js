// Backendcall for RSS-Feed

function rssClick(e){
    currentTime = getCurrentTime();
    callBackEnd(currentTime);
}

function rssCall(){
    currentTime = getCurrentTime();
    callBackEnd(currentTime);
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

function callBackEnd(time){

    var data = "<?xml version='1.0' encoding='UTF-8'?>"
        + "\n<Request>"
        + "\n    <requestName>RSS-Feed<requestName>"
        + "\n    <params>"
        + "\n        <time>2020-07-05 16-36-00</time>"
        + "\n        <numberOfItems>5</numberOfItems>"
        + "\n    </params>"
        + "\n</Request>";

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function() {
        if(this.readyState === 4) {
            console.log(this.responseText);
        }
    });

    xhr.open("GET", "http://127.0.0.1:8082/RSS-Feed");
    xhr.setRequestHeader("Content-Type", "application/xml");

    xhr.send(data);
}

function RSSCallback(oData){
    var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
    transform2(xmlDoc, 'xsl/rssfeednasa.xsl',"mySidebar"); // XSL transformation
    console.log("RSS-Feed");
    //waitForXSL();
}
