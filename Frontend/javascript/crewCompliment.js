// Function that handles click on ISSIcon
var bCrewPopUp = false;
function onBoard(e){  
 
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
  document.getElementById("issOnBoard").style.left=e.originalEvent.x + "px";
  document.getElementById("issOnBoard").style.top=e.originalEvent.y + "px"; 
  console.log("onBoard");
  waitForXSL();
}

function waitForXSL(){
  var slides = document.getElementsByClassName("mySlides");
  if (slides.length!=0) 
  {
  showSlides(1);
  }

  setTimeout(waitForXSL, 50);
} 

// function addBorder(e){
//   console.log("Border");
// }