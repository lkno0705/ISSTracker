function getSliderValue() {
    console.log("getSliderValue");
    var slider = document.getElementById("iss_range");
    var output = document.getElementById("last_pos");
    output.innerHTML = slider.nodeValue;
    
    slider.oninput = function() {
        output.innerHTML = this.value;
        console.log("SLIDER VALUE: " + output.innerHTML);
    }

}

getSliderValue();