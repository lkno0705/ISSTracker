"use strict";

var slideIndex = 1;
var slideIndexTutorial = 1;

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function plusSlidesTutorial(n) {
    showSlidesTutorial(slideIndexTutorial += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function currentSlideTutorial(n) {
    showSlidesTutorial(slideIndexTutorial = n);
}

function closeModal() {
  var modal = document.getElementById("tutorialModal");
  modal.style.display = "none";
}

function openModal() {
  var modal = document.getElementById("tutorialModal");
  modal.style.display = "block";
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
  showSlidesTutorial(1)
}

function showSlides(n) {

    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {
      slideIndex = 1
    }
    if (n < 1) {
      slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
    }
    if (slides.length!=0)
      slides[slideIndex-1].style.display = "block";
    else
      showSlides(n);
}

function showSlidesTutorial(n) {

    var i;
    var slides = document.getElementsByClassName("mySlidesTutorial");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {
      slideIndexTutorial = 1
    }
    if (n < 1) {
      slideIndexTutorial = slides.length
    }
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
    }
    if (slides.length!=0)
      slides[slideIndexTutorial-1].style.display = "block";
    else
      showSlidesTutorial(n);
}