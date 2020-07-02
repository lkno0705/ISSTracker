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
  $.ajax({
    url: 'http://127.0.0.1:8082/AstrosOnISS',
    data:"",
    type: 'GET',
    crossDomain: true,
    dataType: 'xml',
    success: function() { console.log("Success!")},
    error: function() { console.log('Failed!')},
    complete: function(oData){ onBoardCallback(e,oData);}
  });
}

// creation of html DOM
function onBoardCallback(e,oData){
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