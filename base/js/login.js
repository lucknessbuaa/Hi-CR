define(function(require) {
    require('jquery');
    require('bootstrap');
    require('jquery-placeholder');
    require('django-csrf-support');

    $(function() {
        var $tip = null;

        function tip(message) {
            $tip.html(message).hide().fadeIn();
        }

        function login(user, password) {
            return $.post("/login", {
                user: user,
                password: password
            }, 'json').then(function(result) {
                return result.ret_code === 0;
            });
        }

        $form = $("form");
        $form.find("#password, #user").placeholder();
        $tip = $form.find(".alert-danger");
        form = $form[0];
        $submit = $("#submit");
        $form.submit(function(e) {
            e.preventDefault();

            var user = form.user.value;
            var password = form.password.value;
            $submit.button('loading');
            login(user, password).then(function(authenticated) {
                if (!authenticated) {
<<<<<<< HEAD
                    return tip("用户名或密码不正确");
=======
                    return tip("账号或密码不正确");
>>>>>>> hello/master
                }

                window.location = "/welcome";
            }, function() {
                return tip("网络异常");
            }).always(function() {
                $submit.button('reset');
            });
        });
    });
});
