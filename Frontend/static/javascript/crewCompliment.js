"use strict";

// Function that handles click on ISSIcon
var bCrewPopUp = false;
function onBoard(e){  
  changeCursor('wait');
  if (!bCrewPopUp)
  {
  removePopUps();
  bCrewPopUp = true;  
  callBackEnd(e);
  }
}

// Call to back end
function callBackEnd(e){
  var oData = {};
  oData.call = "AstrosOnISS";
  oData.data =  ""
  oData.callback = onBoardCallback;
  oData.type = "GET";
  oData.e = e;
  ajaxCall(oData);
}

// creation of html DOM
function onBoardCallback(oData, e){
  var xmlDoc = oData;
  transform2(xmlDoc, 'xsl/astrosoniss.xsl',"issOnBoard"); // XSL transformation  
  var height=document.getElementById('mapid').offsetHeight;
  var width=document.getElementById('mapid').offsetWidth;
  // get mouse position and set left top corner of div to mouse position
  var y = (200 + e.originalEvent.y);  
  var x = (310 + e.originalEvent.x);  
  if ((310 + e.originalEvent.y) < height) // exception when too closer to border of screen
    document.getElementById("issOnBoard").style.top = e.originalEvent.y + "px"; 
  else
    document.getElementById("issOnBoard").style.top = (height - 240) + "px"; 
  if ((340 + e.originalEvent.x) < width)  // exception when too closer to border of screen
  document.getElementById("issOnBoard").style.left = e.originalEvent.x + "px";
    else
  document.getElementById("issOnBoard").style.left = (width - 340) + "px"; 
  waitForXSL(); // wait for XSLT
}


function waitForXSL(){
  var slides = document.getElementsByClassName("mySlides");
  if (slides.length!=0) // when slider are not empty
  {    
    showSlides(1);
    changeCursor('default');
  } 
  setTimeout(waitForXSL, 50);
} 