define(function() {
    require("jquery");
    require("jquery.iframe-transport");
    var csrf_token = require("django-csrf-support");
    var when = require("when/when");

    var utils = require("js/utils");
    var mapErrors = utils.mapErrors;

    function upload(el) {
        return when($.ajax("/backend/upload/", {
            method: 'POST',
            iframe: true,
            data: {
                csrfmiddlewaretoken: csrf_token
            },
            files: el,
            processData: false,
            dataType: 'json'
        })).then(function(data) {
            return mapErrors(data, function(data) {
                return data.key;
            });
        }, throwNetError);
    }

    return {
        upload: upload,
        getUrl: function(key) {
            return "/backend/upload/" + key;
        }
    };
});