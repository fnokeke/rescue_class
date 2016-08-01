
var rescue_class = function() {

    // #################################################
    // buttons
    // #################################################
    $('#login-btn').click(function() {
        window.location.href = window.location.hostname ==='localhost'
                                  ? 'oauth2callback'
                                  : '/rtime/oauth2callback';
    });

    $('#rescuetime-btn').click(function() {
      //  TODO: check if you can use url_for syntax in javascript
        window.location.href = window.location.hostname ==='localhost'
                                  ? 'rescueOauth2Callback'
                                  : '/rtime/rescueOauth2Callback';
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
