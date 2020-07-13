var bStarted = false;

function getFlyByInfo(latlng,bool){
    // console.log("Now getting infos for: ");
    // console.log(latlng);
    callBackEndFlyBy(latlng);
    callBackEndFutureFlyBy(latlng);   
    if (!bStarted) 
    {   
      start(bool);
      bStarted=true;
    }
      else
    toggleNavL(true);
  }

function callBackEndFlyBy(latlng){
    document.getElementById("pastpasses").innerHTML = "";
    document.getElementById("pastpasses").innerHTML = loadingAnimation;
    document.getElementById("pastpasses").style.minHeight = "200px";

    var oData = {};

    oData.call = "ISSpastPasses";
    oData.data =        "<requestName>ISSpastPasses</requestName>" +
                            "<params>" +
                            "<latitude>" + latlng.lat + "</latitude>" +
                            "<longitude>" + latlng.lng + "</longitude>" +
                            "<radius>" + getRadiusSliderValue() + "</radius>" +
                            "</params>";
    oData.callback = renderFlyBy;
    oData.type = "POST";
    ajaxCall(oData);
   }

   function renderFlyBy(oData){    
    document.getElementById("pastpasses").innerHTML = "";
    document.getElementById("pastpasses").style.minHeight = "";
    if (oData == "error"){
      document.getElementById("pastpasses").innerHTML = "Server error!";
    }    
    if(oData.childNodes[1].childNodes[1].childNodes[1].childNodes.length){
    for (var i = 0; i < oData.childNodes[1].childNodes[1].childNodes[1].childNodes.length; i++) {
      if (oData.childNodes[1].childNodes[1].childNodes[1].childNodes[i].childNodes[0].innerHTML)
      oData.childNodes[1].childNodes[1].childNodes[1].childNodes[i].childNodes[0].innerHTML = parse2localTime(oData.childNodes[1].childNodes[1].childNodes[1].childNodes[i].childNodes[0].innerHTML);
      if (oData.childNodes[1].childNodes[1].childNodes[1].childNodes[i].childNodes[1].innerHTML)
        oData.childNodes[1].childNodes[1].childNodes[1].childNodes[i].childNodes[1].innerHTML = parse2localTime(oData.childNodes[1].childNodes[1].childNodes[1].childNodes[i].childNodes[1].innerHTML);
    }}
    transform2(oData, 'xsl/pastpasses.xsl',"pastpasses"); // XSL transformation
    // console.log("renderFlyBy");
    var objDiv = document.getElementById("leftBottom");
    objDiv.scrollTop = objDiv.scrollHeight;    
}

  function callBackEndFutureFlyBy(latlng){  
    document.getElementById("flyby").innerHTML = "";
    document.getElementById("flyby").innerHTML = loadingAnimation;
    document.getElementById("flyby").style.minHeight = "200px";

    var oData = {};
    
    oData.call = "ISSfuturePasses";
    oData.data =        "<requestName>ISSfuturePasses</requestName>" +
                            "<params>" +
                            "<latitude>" + latlng.lat + "</latitude>" +
                            "<longitude>" + latlng.lng + "</longitude>" +
                            "<number>6</number>" +
                            "</params>";
    oData.callback = renderFutureFlyBy;
    oData.type = "POST";
    ajaxCall(oData);
   }
  
   function renderFutureFlyBy(oData){
    var objDiv = document.getElementById("leftBottom");
    objDiv.scrollTop = objDiv.scrollHeight;  
    if (oData) {
    document.getElementById("flyby").innerHTML = "";
    document.getElementById("flyby").style.minHeight = "";
    for (var i = 0; i < oData.childNodes[1].childNodes[1].childNodes[0].childNodes.length; i++) {
      oData.childNodes[1].childNodes[1].childNodes[0].childNodes[i].firstChild.innerHTML = parse2localTime(oData.childNodes[1].childNodes[1].childNodes[0].childNodes[i].firstChild.innerHTML);
    }
    transform2(oData, 'xsl/flyby.xsl',"flyby"); // XSL transformation
    // console.log("renderFutureFlyBy");     
    }
    else
    document.getElementById("flyby").innerHTML = "<h2>No passes in the near future</h2>";
    objDiv.scrollTop = objDiv.scrollHeight;    
  }