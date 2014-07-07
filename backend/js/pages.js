define(function(require) {
    require("jquery");
    require("jquery.serializeObject");
    require("jquery.iframe-transport");
    require("bootstrap");
    require("parsley");
    var csrf_token = require("django-csrf-support");
    var when = require("when/when");
    var _ = require("underscore");
    require("backbone/backbone");

    var errors = require("errors");

    var utils = require("utils");
    var mapErrors = utils.mapErrors;
    var throwNetError = utils.throwNetError;
    var handleErrors = utils.handleErrors;

    var modals = require('modals');
    var formProto = require("formProto");
    var SimpleUpload = require("simple-upload");

    function modifyPage(data) {
        var request = $.post("/backend/zhaopin/" + data.pk, data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function addPage(data) {
        var request = $.post("/backend/zhaopin/add", data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }
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

    function deletePage(id) {
        var request = $.post("/backend/zhaopin/delete", {
            id: id

        }, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function getUrl(key) {
        return "/backend/upload/" + key;
    }

    var PageForm = Backbone.View.extend(_.extend(formProto, {
        initialize: function() {
            this.setElement($(PageForm.tpl())[0]);
            this.$alert = this.$("p.alert");

        },

        setPage: function(page) {
            _.each(['pk', 'name' , 'judge', 'place' ,'type', 'education', 'examplace','number','workdesc','jobdesc', 'condition'], _.bind(function(attr) {
                if(attr=='judge')
                    this.el[attr].checked = page[attr];
                else
                    this.el[attr].value = page[attr];
            }, this));
        },

        bind: function(data) {
            var defaults = {
                id: '',
                title: '',
                description: '',
                url: ''
            };
            data = _.defaults(data, defaults);
            _.each(['pk','name' , 'judge','place',  'type' , 'education','number', 'examplace','workdesc','jobdesc', 'condition'], _.bind(function(attr) {
                this.el[attr].value = data[attr];
            }, this));
        },

        onShow: function() {
        },

        onHide: function() {
            _.each(['pk', 'name' , 'judge','place' ,'type', 'education','number','examplace','workdesc','jobdesc', 'condition'], _.bind(function(attr) {
                $(this.el[attr]).val('');
            }, this));

            $(this.el).parsley('destroy');
        },

        save: function() {
            var onComplete = _.bind(function() {
                this.trigger('save');
            }, this);

            if (!this.$el.parsley('validate')) {
                return setTimeout(onComplete, 0);
            }

            var onReject = _.bind(function(err) {
                handleErrors(err,
                    _.bind(this.onAuthFailure, this),
                    _.bind(this.onCommonErrors, this),
                    _.bind(this.onUnknownError, this)
                );
            }, this);

            var onFinish = _.bind(function() {
                this.tip('Succeed!', 'success');
                utils.reload(500);
            }, this);

            if (this.el.pk.value !== "") {
                modifyPage(this.$el.serializeObject())
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            } else {
                addPage(this.$el.serializeObject())
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            }
        }
    }));

    $(function() {
        // FIXME
        PageForm.tpl = _.template($("#form_tpl").html());

        var form = new PageForm();
        var modal = new modals.FormModal();
        modal.setForm(form);
        $(modal.el).appendTo(document.body);

        $create = $("#create-page");
        $create.click(function() {
            modal.show();
            modal.setTitle('新增职位信息');
            modal.setSaveText("生成", "生成中...");
        });


        $("table").on("click", ".edit", function() {
            modal.setTitle('编辑职位信息');
            modal.setSaveText("保存", "保存中...");
            var page = $(this).parent().data();
            form.setPage(page);
            modal.show();
        });
    });

    $(function() {
        var modal = new modals.ActionModal();
        modal.setAction(function(id) {
            return deletePage(id).then(function() {
                utils.reload(500);
            }, function(err) {
                if (err instanceof errors.AuthFailure) {
                    window.location = "/welcome";
                }

                throw err;
            });
        });
        modal.setTitle('删除职位信息');
        modal.tip('您确定要<b>删除</b>吗?');
        modal.setSaveText('删除', '删除中...');
        modal.on('succeed', function() {
            utils.reload(500);
        });
        $("table").on("click", ".delete", function() {
            modal.setId($(this).parent().data('pk'));
            modal.show();
        });
    });

    window.onerror = function() {
        console.error(arguments);
    };
});
