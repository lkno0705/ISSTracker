var bStarted = false;

function getFlyByInfo(latlng){
    console.log("Now getting infos for: ");
    console.log(latlng);
    callBackEndFlyBy(latlng);
    callBackEndFutureFlyBy(latlng);   
    if (!bStarted) 
    {   
      start();
      bStarted=true;
    }
      else
    toggleNavL(true);
  }

function callBackEndFlyBy(latlng){
    document.getElementById("pastpasses").innerHTML = "";
    document.getElementById("pastpasses").innerHTML = loadingAnimation;
    $.ajax({
      url: 'http://127.0.0.1:8082/ISSpastPasses',
      data: "<?xml version='1.0' encoding='UTF-8'?>" +
      "<Request>" +
      "<requestName>ISSpastPasses<requestName>" + 
      "<params>" +
      "<latitude>" + latlng.lat + "</latitude>" +
      "<longitude>" + latlng.lng + "</longitude>" +
      "<radius>" + getRadiusSliderValue() + "</radius>" +
      "</params>" +
      "</Request>",
      type: 'POST',
      crossDomain: true,
      dataType: 'xml',
      success: function() { console.log("callBackEndFlyBy Success!")},
      error: function() { console.log('callBackEndFlyBy Failed!')},
      complete: function(oData){renderFlyBy(oData);}
    });
   }

   function renderFlyBy(oData){
    // objDiv.scrollTop = objDiv.scrollHeight;  
    var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
    document.getElementById("pastpasses").innerHTML = "";
    transform2(xmlDoc, 'xsl/pastpasses.xsl',"pastpasses"); // XSL transformation
    console.log("renderFlyBy");
    var objDiv = document.getElementById("mySidebarLeft");
    objDiv.scrollTop = objDiv.scrollHeight;
    //waitForXSL();
}
  

  function callBackEndFutureFlyBy(latlng){  
    document.getElementById("flyby").innerHTML = "";
    document.getElementById("flyby").innerHTML = loadingAnimation;
    $.ajax({
      url: 'http://127.0.0.1:8082/ISSfuturePasses',
      data: "<?xml version='1.0' encoding='UTF-8'?>" +
      "<Request>" +
      "<requestName>ISSfuturePasses<requestName>" + 
      "<params>" +
      "<latitude>" + latlng.lat + "</latitude>" +
      "<longitude>" + latlng.lng + "</longitude>" +
      "<number>6</number>" +
      "</params>" +
      "</Request>",
      type: 'POST',
      crossDomain: true,
      dataType: 'xml',
      success: function() { console.log("callBackEndFutureFlyBy Success!")},
      error: function() { console.log('callBackEndFutureFlyBy Failed!')},
      complete: function(oData){ renderFutureFlyBy(oData);}
    });
   }
  
   function renderFutureFlyBy(oData){
    var objDiv = document.getElementById("mySidebarLeft");
    objDiv.scrollTop = objDiv.scrollHeight;  
    if (oData.responseText)
    {
    var xmlString = oData.responseText;
    var parser = new DOMParser;
    var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
    document.getElementById("flyby").innerHTML = "";
    transform2(xmlDoc, 'xsl/flyby.xsl',"flyby"); // XSL transformation
    console.log("renderFutureFlyBy");   
    // var objDiv = document.getElementById("mySidebarLeft");
    }
    else
    document.getElementById("flyby").innerHTML = "<h2>No passes in the near future</h2>";
    objDiv.scrollTop = objDiv.scrollHeight;    
    //waitForXSL();
}