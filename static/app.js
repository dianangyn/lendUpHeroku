// Execute JavaScript on page load
$(function() {
    // Intercept form submission and submit the form with ajax
    $('#phoneForm').on('submit', function(e) {
        // Prevent submit event from bubbling and automatically
        // submitting the form
        e.preventDefault();

        // Call our ajax endpoint on the server to initialize the
        // phone call
        $.ajax({
            url: '/dial',
            method: 'POST',
            dataType: 'json',
            data: {
                phoneNumber: $('#phoneNumber').val()
            }
        }).done(function(data) {
            // The JSON sent back from the server will contain
            // a success message
            alert(data.message);
        }).fail(function(error) {
            alert(JSON.stringify(error));
        });
    });
});