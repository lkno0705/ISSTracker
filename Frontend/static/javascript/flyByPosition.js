"use strict";

var bStarted = false;

// start flyby infos
function getFlyByInfo(latlng,bool){    
    toggleLoading(false,false,true); // start loading animation
    document.getElementById("flyOver").innerHTML = '<div id=futureContainer><p class="text" style="margin-bottom: -40px;">loading future passes...</p><div id="flyby"></div></div>'+
                                                   '<div id=pastContainer><p class="text"  style="margin-bottom: -40px;">loading past passes...</p><div id="pastpasses"></div></div>'
    document.getElementById("flyby").innerHTML = loadingAnimation; // small animations    
    document.getElementById("pastpasses").innerHTML = loadingAnimation; // small animations
    var bFuture = false;
    var bPast = false;
    callBackEndFutureFlyBy(latlng);    
    if (!bStarted) {   // get left sidebar on first call
      start(bool);
      bStarted = true;
    } else
      toggleNavL(true);
    }
   
      function callBackEndFutureFlyBy(latlng){
        document.getElementById("flyby").style.minHeight = "200px"; // heigth for loading animation
        
        var oData = {}; // object for AJAX call
        oData.e = latlng;
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
      
       function renderFutureFlyBy(oData, latlng){
        if (oData) {
          document.getElementById("futureContainer").innerHTML = '<div id="flyby"></div>';
          document.getElementById("flyby").style.minHeight = "";
    
          // parse all times in table to locale time
          var futurePassDateTime = oData.getElementsByTagName("futurePassDatetime");         
          if( futurePassDateTime.length){
            for (var i = 0; i < futurePassDateTime.length; i++)
            {
                if(futurePassDateTime[i].innerHTML != "")
                futurePassDateTime[i].innerHTML = parse2localTime(futurePassDateTime[i].innerHTML); 
            }
          } 
    
          transform2(oData, 'xsl/flyby.xsl',"flyby"); // XSLT
          }
        else // if no passes
         document.getElementById("flyby").innerHTML = "<h2>No passes in the near future</h2>";    
  
        callBackEndFlyBy(latlng);
      }

function callBackEndFlyBy(latlng){
    document.getElementById("pastpasses").style.minHeight = "200px"; // heigth for loading animation

    var oData = {}; // object for AJAX call

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
    document.getElementById("pastContainer").innerHTML = '<div id="pastpasses"></div>';
    document.getElementById("pastpasses").style.minHeight = "";
    if (oData == "error"){
      document.getElementById("pastpasses").innerHTML = "<p class='text'>Server error!</p>";
      toggleLoading(true);
      bGeoCodingInProgress = false;
      bFromMarker = false;    
      return;
    }    
    // parse all times in table to locale time
    var startTimes = oData.getElementsByTagName("startTime");
    var endTimes = oData.getElementsByTagName("endTime");
    if( startTimes.length){
      for (var i = 0; i < startTimes.length; i++)
      {
          if(startTimes[i].innerHTML != "")
              startTimes[i].innerHTML = parse2localTime(startTimes[i].innerHTML);
          if(endTimes[i].innerHTML != "")
              endTimes[i].innerHTML = parse2localTime(endTimes[i].innerHTML);
      }
    } 
    transform2(oData, 'xsl/pastpasses.xsl',"pastpasses"); // XSLT
    toggleLoading(true); // remove loading screen  
    bGeoCodingInProgress = false;
    bFromMarker = false;
}