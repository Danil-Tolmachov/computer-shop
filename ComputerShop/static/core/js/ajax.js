
$(document).ready(function() {
$(document).on('click', '.del-item', function() {
  	    let id = $(this).attr('id');
        let token = $('.cart-items [name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: 'http://' + document.location.host + '/cart-delete/',
            type: 'post',
            data: {
                'id':id,
                'csrfmiddlewaretoken': token,
            },

            success: function(data) {
                $('#'+id).closest('.cancel').slideUp(300);
                setTimeout(() => $('#'+id).closest('.cancel').remove() , 300);

                $('#'+id).closest('.cancel').slideUp(300);
                setTimeout(() => $('#'+id).closest('.cancel').remove() , 300);
            },

            error: function(error) {
                alert(error);
            }
        })
    },
)

$(document).on('click', '.add-item', function() {
  	    let id = parseInt($(this).attr('id').split('/')[1]);
        let token = $('.cart-items [name="csrfmiddlewaretoken"]').val();


        $.ajax({
            url: 'cart-add/',
            type: 'post',
            data: {
                'id': id,
                'csrfmiddlewaretoken': token,
            },

            success: function(data) {
                let itemDiv = `<div class="cancel"><a href="/product/${data['pk']}/">${data['name']}</a><button class="fa-solid fa-xmark del-item" id="${data['pk']}"></button></div>`;

                $('.cart-items').prepend(itemDiv.replace(/\r?\n/g, ""))
                },

            error: function(error) {
                alert(error);
            }
        })
    },
)
})