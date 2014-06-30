define(function(require) {
    require("jquery");
    require("jquery.serializeObject");
    require('jquery-placeholder');
    require("jquery.iframe-transport");
    require("bootstrap");
    require("select2");
    require("jquery.ui.sortable");
    require("parsley");
    var radiu = require('radiu');
    var csrf_token = require("django-csrf-support");
    var when = require("when/when");
    var _ = require("underscore");
    require("backbone/backbone");

    var multiline = require("multiline");

    var errors = require("errors");
    var utils = require("utils");
    var mapErrors = utils.mapErrors;
    var throwNetError = utils.throwNetError;
    var handleErrors = utils.handleErrors;
    var formProto = require("formProto");
    var formValidationProto = require("formValidationProto");
    var modals = require('modals');

    function queryPages(term) {
        var request = $.get("/backend/dialogs/pages", {
            term: term || ""
        }, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    var availablePages = [];
    queryPages().then(_.bind(function(data) {
        availablePages = data.pages;
    }, this));

    function EventKeyDuplicatedError() {}

    function SubscribeDuplicatedError() {}

    var EVENTKEY_DUPLICATED = 2001;
    var SUBSCRIBE_DUPLICATED = 2002;

    function mapDialogErrors(result, fn) {
        switch (result.ret_code) {
            case EVENTKEY_DUPLICATED:
                throw new EventKeyDuplicatedError();
            case SUBSCRIBE_DUPLICATED:
                throw new SubscribeDuplicatedError();
        }

        return _.isFunction(fn) ? fn.call(null, result) : result;
    }

    function modifyTalk(data) {
        var request = $.post("/backend/talk" + data.pk, data, 'json');
        return when(request).then(function(result) {
            return mapErrors(result, mapDialogErrors);
        }, throwNetError);
    }

    function addDialog(data) {
        var request = $.post("/backend/dialogs/add", data, 'json');
        return when(request).then(function(result) {
            return mapErrors(result, mapDialogErrors);
        }, throwNetError);
    }

    function deleteDialog(id) {
        var request = $.post("/backend/dialogs/delete", {
            id: id
        }, 'json');
        return when(request).then(function(result) {
            return mapErrors(result, mapDialogErrors);
        }, throwNetError);
    }

    function Dialog(options) {
        var attrs = ['name', 'pk', 'event', 'text', 'response', 'page', 'key']
        _.extend(this, _.pick(options, attrs));
    }

    _.extend(Dialog.prototype, {
        getInputType: function() {
            return this.text !== '' ? 'text' : 'event';
        },

        getOutputType: function() {
            return this.response !== '' ? 'text' : 'page';
        }
    });


    var proto = _.extend({}, formProto, formValidationProto);
    var DialogForm = Backbone.View.extend(_.extend(proto, {
        initialize: function() {
            this.setElement($.parseHTML(DialogForm.tpl().trim())[0]);
            this.$alert = this.$("p.alert");
            this.$textGroup = this.$(".group-text");
            this.$eventGroup = this.$(".group-event");
            this.$pageGroup = this.$(".group-page");
            this.$pages = $(this.el.pages);
            this.$responseGroup = this.$(".group-response");
            this.$key = this.$("[name=key]");
            this.$key.placeholder();
            this.$(".glyphicon-info-sign").tooltip();
        },

        events: {
            'change [name=outputType]': 'onOutputTypeChanged',
            'change [name=inputType]': 'onInputTypeChanged',
            'change [name=event]': 'onEventTypeChaned'
        },

        onOutputTypeChanged: function() {
            if (radiu.value($(this.el.outputType)) === 'text') {
                this.$pageGroup.addClass("hide");
                this.$responseGroup.removeClass("hide");
            } else {
                this.$pageGroup.removeClass("hide");
                this.$responseGroup.addClass("hide");
            }
        },

        destroySelect: function() {
            this.$pages.select2('destroy');
        },

        initSelect: function() {
            var pageTpl = _.template(multiline(function() {
                /*@preserve
                <span class='text-primary glyphicon glyphicon-link'></span>&nbsp;
                <%= name %>
                */
                console.log
            }));

            function format(data) {
                return pageTpl(data);
            }

            this.$pages.select2({
                multiple: true,
                data: availablePages,
                formatSelection: format,
                formatResult: format,
                initSelection: _.bind(function(el, callback) {
                    var items = this.pages === "" ? [] : this.pages.split(",");
                    items = _.map(items, function(item) {
                        return parseInt(item);
                    });

                    var results = [];
                    for (var i = 0; i < items.length; i++) {
                        var item = items[i];
                        for (var j = 0; j < availablePages.length; j++) {
                            if (availablePages[j].id === item) {
                                results.push(availablePages[j]);
                                break;
                            }
                        }
                    }
                    callback(results);
                }, this)
            });

            this.$pages.select2('container').find('ul.select2-choices').sortable({
                containment: 'parent',
                start: _.bind(function() {
                    this.$pages.select2('onSortStart');
                }, this),
                update: _.bind(function() {
                    this.$pages.select2('onSortEnd');
                }, this)
            });

            this.$pages.select2('val', this.pages);
        },

        onShow: function() {
            this.initSelect();
        },

        onInputTypeChanged: function() {
            if (radiu.value($(this.el.inputType)) === 'text') {
                this.$textGroup.removeClass("hide");
                this.$eventGroup.addClass("hide");
            } else {
                this.$textGroup.addClass("hide");
                this.$eventGroup.removeClass("hide");
            }
        },

        getEventType: function() {
            return this.el.event.value;
        },

        setEventType: function(type) {
            $(this.el.event).val(type).trigger('change');
        },

        setInputType: function(type) {
            radiu.check($(this.el.inputType), type);
            $(this.el.inputType).trigger('change');
        },

        setOutputType: function(type) {
            radiu.check($(this.el.outputType), type);
            $(this.el.outputType).trigger('change');
        },

        onEventTypeChaned: function() {
            if (this.getEventType() === 'click') {
                this.$key.parent().removeClass('hide');
            } else {
                this.$key.parent().addClass('hide');
            }
        },

        clear: function() {
            _.each(['pk', 'name', 'text', 'key', 'pages', 'response'], _.bind(function(field) {
                $(this.el[field]).val('');
            }, this));

            this.setInputType('text');
            this.setOutputType('text');
            this.setEventType('subscribe');
        },

        setDialog: function(dialog) {
            this.dialog = new Dialog(dialog);
            $(this.el.name).val(dialog.name);
            $(this.el.pk).val(dialog.pk);
            if (this.dialog.getInputType() === 'event') {
                this.setInputType('event');
                this.setEventType(this.dialog.event);
                if (this.dialog.event !== 'subscribe') {
                    $(this.el.key).val(dialog.key);
                }
            } else {
                $(this.el.text).val(dialog.text);
            }

            this.setOutputType(this.dialog.getOutputType());
            if (this.dialog.getOutputType() === 'page') {
                this.pages = dialog.pages.toString();
            } else {
                this.el.response.value = dialog.response;
            }
        },

        bind: function(data) {},

        onShow: function() {
            this.initSelect();
        },

        onHide: function() {
            this.clear();
            this.clearErrors(["name", "text", "key", "pages", "response"])
            this.pages = '';
            this.destroySelect();
            this.clearTip();
        },

        getData: function() {
            var data = this.$el.serializeObject();
            if (data.inputType === 'text') {
                data.event = '';
                data.key = '';
            } else {
                data.text = '';
            }

            if (data.outputType === 'page') {
                data.response = '';
            } else {
                data.page = '';
            }

            return data;
        },

        validate: function() {
            this.clearErrors(["name", "text", "key", "pages", "response"])

            if (this.el.name.value === "") {
                this.addError(this.el.name, 'This field is required');
                return false;
            }

            if (radiu.value($(this.el.inputType)) === 'text') {
                if (this.el.text.value === "") {
                    this.addError(this.el.text, 'This field is required');
                    return false;
                }
            } else if (this.getEventType() === 'click' && this.el.key.value === "") {
                this.addError(this.el.key, 'This field is required');
                return false;
            }

            if (radiu.value($(this.el.outputType)) === 'text') {
                if (this.el.response.value === "") {
                    this.addError(this.el.response, 'This field is required');
                    return false;
                }
            } else if ($(this.el.pages).val() === "") {
                this.addError(this.el.pages, 'This field is required');
                return false;
            } else {
                var pages = $(this.el.pages).val().split(",");
                if (pages.length > 10) {
                    this.addError(this.el.pages, 'Not more than 10 pages');
                    return false;
                }
            }

            return true;
        },

        save: function() {
            var onComplete = _.bind(function() {
                this.trigger('save');
            }, this);

            if (!this.validate()) {
                return setTimeout(onComplete, 0);
            }

            var onReject = _.bind(function(err) {
                handleErrors(err,
                    _.bind(this.onAuthFailure, this),
                    _.bind(this.onCommonErrors, this),
                    _.bind(function(err) {
                        if (err instanceof SubscribeDuplicatedError) {
                            // TODO 修改wording
                            this.tip('Subscribe event has been used', 'danger');
                            return true;
                        }
                    }, this),
                    _.bind(function() {
                        if (err instanceof EventKeyDuplicatedError) {
                            // TODO 修改wording
                            this.tip('Duplicated event key', 'danger');
                            return true;
                        }
                    }, this),
                    _.bind(this.onUnknownError, this)
                );
            }, this);

            var onFinish = _.bind(function() {
                this.tip('Succeed!', 'success');
                utils.reload(500);
            }, this);

            var data = this.getData();

            if (this.el.pk.value !== "") {
                modifyDialog(data)
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            } else {
                addDialog(data)
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            }
        }
    }));

    $(function() {
        // FIXME
        DialogForm.tpl = _.template($("#form-tpl").html());

        var form = new DialogForm();
        var modal = new modals.FormModal();
        modal.setForm(form);
        $(modal.el).appendTo(document.body);

        $create = $("#create-dialog");
        $create.click(function() {
            modal.show();
            modal.setTitle('Create Dialog');
            modal.setSaveText("Create", "Creating...");
        });

        $("table").on("click", ".edit", function() {
            modal.setTitle('Edit Dialog');
            modal.setSaveText("Save", "Saving...");
            var dialog = $(this).parent().data();
            form.setDialog(dialog);
            modal.show();
        });
    });

    $(function() {
        var modal = new modals.ActionModal();
        modal.setAction(function(id) {
            return deleteDialog(id).then(function() {
                utils.reload(500);
            }, function(err) {
                if (err instanceof errors.AuthFailure) {
                    window.location = "/welcome";
                }

                throw err;
            });
        });
        modal.setTitle('Delete Dialog');
        modal.tip('Are you <b>ABSOLUTELY</b> sure?');
        modal.setSaveText('delete', 'delete...');
        $("table").on("click", ".delete", function() {
            modal.setId($(this).parent().data('pk'));
            modal.show();
        });
    });
});
