
var rescue_class = function() {

    // #################################################
    // buttons
    // #################################################
    $('#login-btn').click(function() {
        window.location.href = '/oauth2callback';
    });

    $('#rescuetime-btn').click(function() {
        window.location.href = '/rescueOauth2Callback';
    });


    // #################################################
    // page animation for message
    // #################################################
    $(".alert-dismissible").each(function(index) {
        var $me = $(this);
        $me.delay(2000 + 800 * index).fadeTo(200, 0).slideUp(200,
            function() {
                $me.alert('close');
            });
    });
};

$(document).ready(function() {
    rescue_class();
});
