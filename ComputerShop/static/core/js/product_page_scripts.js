$(document).ready(function () {

    /* Specifications */
    let container = $('.specifications');
    let specs = $('.specs-footer');
    let table = $('.spec-table');
    const short = $('.detail-specs').height()


    if ( $('.specs-footer i').length != 0 ) {

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
            
    }
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

    /* Add Comment */
    $(document).on('click', '.add-comment', function() {
        let id = $(this).attr('id');
        let token = $('input[name="csrfmiddlewaretoken"]').val();
        let content = $('#comment-content').val();
        let is_positive = ($('#is_positive').is(':checked') === true) ? 1 : 0;
        
        $.ajax({
            url: 'http://' + document.location.host + '/add-comment/',
            type: 'post',
            data: {
                'product': id,
                'content': content,
                'is_positive': is_positive,
                'csrfmiddlewaretoken': token,
            },
          
            success: function(data) {
                location.reload();
            },
          
            error: function(xhr, ajaxOptions, thrownError) {
                let messageWindow = $('.message-window-container');
                title = $('.message-window-container p[name="title"]');
                text = $('.message-window-container p[name="text"]');

                let message = JSON.parse(xhr.responseText)['error'];

                title.text('Error');
                text.text(`${message}`);

                messageWindow.fadeIn(200);
    
            }
        })
    },

    )
    /* /Add Comment */

})
