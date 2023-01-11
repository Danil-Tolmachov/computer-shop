$(document).ready( function() {

    let token = $('.cart-items [name="csrfmiddlewaretoken"]').val();

    // Change password query
    $('#change-password-form').click( function() {

        // Get password
        var password = $('#change-password-form').siblings('input[name="password"]').val()
        var newPassword1 = $('#change-password-form').siblings('input[name="new_password1"]').val()
        var newPassword2 = $('#change-password-form').siblings('input[name="new_password2"]').val()

        var changePasswordFormData = {

            password: password,
            new_password1: newPassword1,
            new_password2: newPassword2,
            'csrfmiddlewaretoken': token,
        };


        $.ajax({
            type: "POST",
            url: "http://" + document.location.host + "/account/change-password",
            data: changePasswordFormData,
            dataType: "json",
            encode: true,
        

            success: function(data) {
                let messageWindow = $('.message-window-container')
                title = $('.message-window-container p[name="title"]')
                text = $('.message-window-container p[name="text"]')

                let message = "Password was changed successfuly"

                title.text('Success')
                text.text(message)

                messageWindow.fadeIn(200)

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

    // Change email query
    $('#change-email-form').click( function() {

        // Get password
        var password = $('#change-email-form').siblings('input[name="password"]').val()

        var changeEmailFormData = {
            password: password,
            new_email1: $('input[name="new_email1"]').val(),
            new_email2: $('input[name="new_email2"]').val(),
            'csrfmiddlewaretoken': token,
        };

        $.ajax({
            type: "POST",
            url: "http://" + document.location.host + "/account/change-email",
            data: changeEmailFormData,
            dataType: "json",
            encode: true,


            success: function(data) {
                let messageWindow = $('.message-window-container')
                title = $('.message-window-container p[name="title"]')
                text = $('.message-window-container p[name="text"]')

                let newEmail = data['new_email']

                title.text('Success')
                text.text(`Successfuly changed email to ${newEmail}`)

                $('dd[name="Email"]').text(data['new_email'])

                messageWindow.fadeIn(200)

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

})