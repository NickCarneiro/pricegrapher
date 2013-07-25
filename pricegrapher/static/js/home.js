$(function() {

    $('#url-submit').on('click', function() {
        lookupUrl();
    });
    $('#url-input').on('keypress', function(e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        if(code == 13) { //Enter keycode
            lookupUrl();
        }

    });
    function lookupUrl() {
        $.ajax('/lookup/', {
            type: 'POST',
            success: function(res) {
                if (res.redirectUrl !== undefined) {
                    //go to the product url
                    document.location = res.redirectUrl;
                } else if (res.error) {
                    //show error
                    var error = res.error;
                    $('#error-block').text(error);
                } else {
                    $('error-block').text("Something went wrong on our end. Try again later.");
                }
            },
            error: function(res) {
                $('#error-block').html("Something went wrong on our end. <br />Try again later?");
            },
            data: {
                'productUrl': $('#url-input').val()
            }
        });
    }

});