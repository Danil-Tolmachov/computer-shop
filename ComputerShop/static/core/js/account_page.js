$(document).ready( function() {


    // Left nav buttons
    $('.left-nav button').click( function() {
        let id = $(this).attr('id');

        $('.menu-page').hide().css('opacity', '0.3');
        $($('.menu-page')[id]).show().animate({opacity: 1}, 300);

        if (id == 0) {
            $('.account-inner').css('border-bottom-right-radius', '35px');
        }
        else {
            $('.account-inner').css('border-bottom-right-radius', '12px');
        }
    })


    // Change something button
    $('#change-button').click( function() {

        if ($(".menu-page dd[is_changeable='True'] input").length > 0) {
            return;
        }

        let changeable_fields = $(".menu-page dd[is_changeable='True']");

        changeable_fields.each(function(iter, elem) {
            let content = $(elem).text().trim();
            let name = $(elem).attr('name');

            $(elem).empty();
            $(elem).append(`<input name="${name}" placeholder="${content}" class="account-field">`).hide();
            $(elem).fadeIn(300)
        })
    })

})