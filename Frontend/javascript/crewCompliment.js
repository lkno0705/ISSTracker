
function callBackEnd(){
  $.ajax({
    url: 'http://127.0.0.1:8082',
    data:"AstrosOnISS",
    type: 'GET',
    crossDomain: true,
    dataType: 'json',
    success: function() { console.log("Success"); },
    error: function() {  console.log('Failed!'); }
})
}
// callBackEnd();

function onBoard(e){
  removePopUps();
  transform('xml/astosoniss.xml', 'xsl/astrosoniss.xsl',"issOnBoard");
  var xpos = document.getElementById("issOnBoard").style.left=e.originalEvent.x + "px";
  var ypos = document.getElementById("issOnBoard").style.top=e.originalEvent.y + "px";
  var divHeight = document.getElementById("issOnBoard").style.height;
  var divWidth = document.getElementById("issOnBoard").style.width;
  console.log("xpos: " + xpos + " | ypos: " + ypos + " | divHeight: " + divHeight + " | divWidth: " + divWidth);
  console.log("onBoard");
}