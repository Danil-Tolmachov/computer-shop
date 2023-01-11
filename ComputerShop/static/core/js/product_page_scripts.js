$(document).ready(function () {

    /* Specifications */
    let container = $('.specifications');
    let specs = $('.specs-footer');
    let table = $('.spec-table');
    const short = $('.detail-specs').height()
    let animationTime = parseInt(parseFloat($('.specs-footer i').css('transition-duration').slice(0, -1))*500)

    $(specs).click(function () {
        if (container.height() <= 220){
            container.animate({'height': container.height() - $('.detail-specs').height() + table.height() + 'px'}, animationTime);
            $('.specs-footer i').css('transform', 'rotate(180deg)')
        } else {
            container.animate({'height':container.height() - table.height() + short + 'px'}, animationTime)
            $('.specs-footer i').css('transform', 'rotate(0deg)')
        }
    })
    /* /Specifications */


    /* Carousel */
    const slides = $('.carousel-item');

    $(slides[0]).css("opacity", 1);

    slides.each((indx, slide) => {
        slide.style.transform = `translateX(${indx * 100}%)`;
    });


    const nextSlide = $('.carousel-arrow-right');

    let curSlide = 0;
    let maxSlide = slides.length - 1;

    nextSlide.click( function () {
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

      slides.each((indx, slide) => {
        slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
      });
    });

    const prevSlide = $(".carousel-arrow-left");

    prevSlide.click( function () {
      if (curSlide === 0) {
      	slides[curSlide].style.opacity = 0;
        curSlide = maxSlide;
        slides[curSlide].style.opacity = 1;

      } else {
      	slides[curSlide].style.opacity = 0;
        curSlide--;
        slides[curSlide].style.opacity = 1;
      }

      slides.each((indx, slide) => {
        slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
      });
    });
    /* /Carousel */

})
