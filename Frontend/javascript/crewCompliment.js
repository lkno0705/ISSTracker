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
  var xmlString = oData.responseText;
  var parser = new DOMParser; 
  var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
  transform2(xmlDoc, 'xsl/astrosoniss.xsl',"issOnBoard"); // XSL transformation  
  var height=document.getElementById('mapid').offsetHeight;
  var width=document.getElementById('mapid').offsetWidth;
  var y = (200 + e.originalEvent.y);
  var x = 310 + e.originalEvent.x;
  if ((310 + e.originalEvent.y) < height)
    document.getElementById("issOnBoard").style.top = e.originalEvent.y + "px"; 
  else
    document.getElementById("issOnBoard").style.top = (height - 240) + "px"; 
  if ((340 + e.originalEvent.x) < width)
  document.getElementById("issOnBoard").style.left = e.originalEvent.x + "px";
    else
  document.getElementById("issOnBoard").style.left = (width - 340) + "px";
  
  console.log("onBoard");
  waitForXSL();
}

function waitForXSL(){
  var slides = document.getElementsByClassName("mySlides");
  if (slides.length!=0) 
  {    
    showSlides(1);
    changeCursor('default');
  } 
  setTimeout(waitForXSL, 50);
} 