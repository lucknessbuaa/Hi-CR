define(function(require) {
    require("jquery");
    var errors = require("errors");

    var formProto = {
        onAuthFailure: function(err) {
            if (err instanceof errors.AuthFailure) {
                window.location = "/welcome";
                return true;
            }
        },

        onCommonErrors: function(err) {
            if (err instanceof errors.NetworkError) {
                this.tip('网络错误!', 'danger');
                return true;
            } else if (err instanceof errors.InternalError) {
                this.tip('服务器错误!', 'danger');
                return true;
            } else if (err instanceof errors.FormInvalidError) {
                this.tip('服务器错误!', 'danger');
                return true;
            }
        },

        onUnknownError: function(err) {
            this.tip('Error!', 'danger');
            return true;
        },

        tip: function(msg, type) {
            this.$alert.hide();
            var classname = "alert-" + type;
            this.$alert.attr("class", "alert " + classname).html(msg).show();
        },

        clearTip: function() {
            this.$alert.hide().empty().attr('class', "alert");
        }
    }

    return formProto;
});
