// Function that handles click on ISSIcon
function onBoard(e){
  removePopUps();
  callBackEnd(e);
}

// Call to back end
function callBackEnd(e){
  $.ajax({
    url: 'http://127.0.0.1:8082',
    data:"AstrosOnISS",
    type: 'GET',
    crossDomain: true,
    dataType: 'xml',
    success: function(data) { console.log("Success!")},
    error: function(data) { console.log('Failed!')},
    complete: function(data){ onBoadCallback(e,data);}
  });
}

// creation of html DOM
function onBoadCallback(e,data){
  var xmlString ='<?xml version="1.0" encoding="UTF-8"?><Request><requestName>AstrosOnISS</requestName><data><Astro name="Chris Cassidy"><picture>https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/JohnCassidyv2.jpg/300px-JohnCassidyv2.jpg</picture><flag>https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/220px-Flag_of_the_United_States.svg.png</flag><nation>USA</nation></Astro><Astro name="Anatoly Ivanishin"><picture>https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Anatoli_Ivanishin_2011.jpg/300px-Anatoli_Ivanishin_2011.jpg</picture><flag>https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/255px-Flag_of_Russia.svg.png</flag><nation>Russia</nation></Astro><Astro name="Ivan Vagner"><picture>https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Ivan_Vagner_%28Jsc2020e014992%29.jpg/330px-Ivan_Vagner_%28Jsc2020e014992%29.jpg</picture><flag>https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/255px-Flag_of_Russia.svg.png</flag><nation>Russia</nation></Astro><Astro name="Doug Hurley"><picture>https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Douglas_Hurley.jpg/200px-Douglas_Hurley.jpg</picture><flag>https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/220px-Flag_of_the_United_States.svg.png</flag><nation>USA</nation></Astro><Astro name="Bob Behnken"><picture>https://de.wikipedia.org/wiki/Datei:Robertbehnkenv2.jpg</picture><flag>https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/220px-Flag_of_the_United_States.svg.png</flag><nation>USA</nation></Astro></data></Request>'
  var parser = new DOMParser; 
  var xmlDoc = parser.parseFromString(xmlString, "text/xml"); // XML creation
  transform2(xmlDoc, 'xsl/astrosoniss.xsl',"issOnBoard"); // XSL transformation
  var xpos = document.getElementById("issOnBoard").style.left=e.originalEvent.x + "px";
  var ypos = document.getElementById("issOnBoard").style.top=e.originalEvent.y + "px"; 
  console.log("onBoard");
  waitForXSL();
}

function waitForXSL(){
  var slides = document.getElementsByClassName("mySlides");
  if (slides.length!=0) 
  showSlides(1);

  setTimeout(waitForXSL, 50);
} 