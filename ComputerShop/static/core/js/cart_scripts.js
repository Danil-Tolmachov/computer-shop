$(document).ready( function() {


    /* Cart */
    $(document).on('click', '.del-item-cart.cart-page', function() {
        let id = $(this).attr('id');
        let token = $('.products-inner [name="csrfmiddlewaretoken"]').val();
        
        $.ajax({
            url: 'http://' + document.location.host + '/cart-delete/',
            type: 'post',
            data: {
                'id':id,
                'csrfmiddlewaretoken': token,
            },
          
            success: function(data) {
                $('#'+id).closest('.cart-product').animate({opacity: 0 }, 200).animate({ height: 0 }, 300);
                setTimeout(() => $('#'+id).closest('.cancel').remove() , 300);
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
    })

    $('.product-cart-count').change( function () {
        let id = $(this).attr('id');
        let token = $('.products-inner [name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: 'http://' + document.location.host + '/cart-set/',
            type: 'post',
            data: {
                'id': id,
                'count': parseInt($(this).val()),
                'csrfmiddlewaretoken': token,
            },
        
            success: function(data) {
                console.dir(data);
                $('#summary').animate({opacity: 0.3 }, 200);
                setTimeout(() => $('#summary').text('Summary: $' + data['summary']), 200);
                $('#summary').animate({opacity: 1 }, 100);;
            },
            
            error: function(xhr, ajaxOptions, thrownError) {
            }
        })
    /* /Cart */
    })
})
