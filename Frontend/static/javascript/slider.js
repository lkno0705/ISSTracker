"use strict";

function getSliderValue() {
    var slider = document.getElementById("iss_range");
    var output = document.getElementById("last_pos");
    output.innerHTML = slider.value*10;

    slider.oninput = function() {
        output.innerHTML = this.value*10;
    }
    return parseInt(output.innerHTML);
}

function getRadiusSliderValue(){
  var slider = document.getElementById("position_radius");
  var output = document.getElementById("radius");
  output.innerHTML = slider.value;

  slider.oninput = function() {
    output.innerHTML = this.value;
    if (circle)
      circle.setRadius(this.value*1000)
  }  
  return parseInt(output.innerHTML);
}

function sliderRadiusMoved(){
  if(posMarker)
  {
    getFlyByInfo(posMarker._latlng);
  }
}

// function to get slider time
function getSliderTime() {
  return getCurrentTime(getSliderValue());
}
function sliderTimeMoved(){
  callBackEndISSDB()
}