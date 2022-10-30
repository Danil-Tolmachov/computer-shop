"use strict";
// Select all slides
const slides = document.querySelectorAll('.carousel-item');

slides[0].style.opacity = 1;

// loop through slides and set each slides translateX
slides.forEach((slide, indx) => {
  slide.style.transform = `translateX(${indx * 100}%)`;
});


// select next slide button
const nextSlide = document.querySelector('.carousel-arrow-right');

// current slide counter
let curSlide = 0;
// maximum number of slides
let maxSlide = slides.length - 1;

// add event listener and navigation functionality
nextSlide.addEventListener("click", function () {
  // check if current slide is the last and reset current slide
  if (curSlide === maxSlide) {
  	slides[curSlide].style.opacity = 0;
    curSlide = 0;
   	slides[curSlide].style.opacity = 1;
   	
  } else {
  	slides[curSlide].style.opacity = 0;
    curSlide++;
    slides[curSlide].style.opacity = 1;
  }

  //   move slide by -100%
  slides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
  });
});

// select next slide button
const prevSlide = document.querySelector(".carousel-arrow-left");

// add event listener and navigation functionality
prevSlide.addEventListener("click", function () {
  // check if current slide is the first and reset current slide to last
  if (curSlide === 0) {
  	slides[curSlide].style.opacity = 0;
    curSlide = maxSlide;
    slides[curSlide].style.opacity = 1;

  } else {
  	slides[curSlide].style.opacity = 0;
    curSlide--;
    slides[curSlide].style.opacity = 1;
  }

  //   move slide by 100%
  slides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
  });
});
