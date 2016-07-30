
var rescue_class = function () {

    $('#login-btn').click(function() {
      window.location.href = '/oauth2callback';
    });
};

$(document).ready(function() {
  rescue_class();
});
