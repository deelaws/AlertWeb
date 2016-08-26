$(function () {
    $('.activateButton').bind('click', function (sender) {
        var alert_id = sender.toElement.parentElement.id;
        $.ajax({
            url: '/rescue/activate',
            data: {"alertid": alert_id },
            type: 'POST',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});