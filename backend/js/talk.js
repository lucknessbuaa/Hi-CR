define(function(require) {
    require("jquery");
    require("jquery.serializeObject");
    //require('jquery-placeholder');
    require("jquery.iframe-transport");
    require("bootstrap");
    require("moment");
    require("bootstrap-datetimepicker");
    require("select2");
    //require("jquery.ui.sortable");
    require("parsley");
    //var radiu = require('radiu');
    var csrf_token = require("django-csrf-support");
    var when = require("when/when");
    var _ = require("underscore");
    require("backbone/backbone");

    //var multiline = require("multiline");

    var errors = require("errors");
    var utils = require("utils");
    var mapErrors = utils.mapErrors;
    var throwNetError = utils.throwNetError;
    var handleErrors = utils.handleErrors;
    var formProto = require("formProto");
    var formValidationProto = require("formValidationProto");
    var modals = require('modals');
    var SimpleUpload = require("simple-upload");


    function modifyTalk(data) {
        var request = $.post("/backend/talk/" + data.pk, data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function addTalk(data) {
        var request = $.post("/backend/talk/add", data, 'json');
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

    function deleteTalk(id) {
        var request = $.post("/backend/talk/delete", {
            id: id
        }, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function requireUni() {
        var request = $.post("/backend/talk/requireUni", 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function requireCity() {
        var request = $.post("/backend/talk/requireCity", 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    var selectCity = [];
    requireCity().then(_.bind(function(data) {
        selectCity = data.selectCity;
    }, this));

    var selectUni = [];
    requireUni().then(_.bind(function(data) {
        selectUni = data.selectUni;
    }, this));

    var proto = _.extend({}, formProto, formValidationProto);
    var TalkForm = Backbone.View.extend(_.extend(proto, {
        initialize: function() {
            this.setElement($.parseHTML(TalkForm.tpl().trim())[0]);
            this.$alert = this.$("p.alert");
            this.$(".glyphicon-info-sign").tooltip();
        },

        setDate: function() {
            this.$("[name=wtdate]").attr({
                readOnly: "true"
            });
            this.$("[name = date]").attr({
                readOnly: "true"
            });
            this.$("[name = date]").datetimepicker({
                maxView: 2,
                minView: 0,
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
            });
            this.$("[name = wtdate]").datetimepicker({
                maxView: 2,
                minView: 0,
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
            });

            this.$("[name = date]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
            this.$("[name = wtdate]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        },

        setTalk: function(talk) {
            _.each(['pk', 'city', 'university', 'date', 'place', 'capacity', 'speaker', 'wtdate'], _.bind(function(attr) {
                this.el[attr].value = talk[attr];
            }, this));

            var tempTime1 = moment(talk['date'], "MMM DD,YYYY,h:m a");
            this.el['date'].value = tempTime1.format("YYYY - MM - DD HH: mm");
            var tempTime = moment(talk['wtdate'], "MMM DD,YYYY,h:m a");
            this.el['wtdate'].value = tempTime.format("YYYY-MM-DD HH:mm");
        },


        bind: function(data) {
            var defaults = {
                id: '',
                title: '',
                description: '',
                url: ''
            };
            data = _.defaults(data, defaults);
            _.each(['pk', 'city', 'university', 'date', 'place', 'capacity', 'speaker', 'wtdate'], _.bind(function(attr) {
                this.el[attr].value = data[attr];
            }, this));
        },

        onCityChanged: function() {
            this.$("[name=university]").select2({
                query: function(query) {
                    var data = {
                        results: []
                    };
                    for (var i = 0; i < selectUni.length; i++) {
                        if (selectUni[i].city == document.getElementById('id_city').value) {
                            data.results.push(selectUni[i]);
                        }
                    }
                    query.callback(data);
                }
            });
        },

        initSelect: function() {
            this.$("[name=city]").select2({
                data: selectCity,
            });
        },


        onShow: function() {
            this.setDate();
            this.onCityChanged();
            this.initSelect();
        },

        clear: function() {
            _.each(['pk', 'city', 'university', 'date', 'place', 'capacity', 'speaker', 'wtdate'], _.bind(function(field) {
                $(this.el[field]).val('');
            }, this));
        },

        onHide: function() {
            this.clear();
            this.clearErrors(['city', 'university', 'date', 'place', 'capacity', 'speaker', 'wtdate'])
            $(this.el).parsley('destroy');
        },

        getData: function() {
            var data = this.$el.serializeObject();

            return data;
        },

        validate: function() {
            this.clearErrors(['city', 'university', 'date', 'place', 'capacity', 'speaker', 'wtdate']);

            if (this.el.city.value === "") {
                this.addError(this.el.city, 'This field is required');
                return false;
            }
            if (this.el.university.value === "") {
                this.addError(this.el.university, 'This field is required');
                return false;
            }
            if (this.el.date.value === "") {
                this.addError(this.el.date, 'This field is required');
                return false;
            }
            if (this.el.place.value === "") {
                this.addError(this.el.place, 'This field is required');
                return false;
            }
            if (this.el.capacity.value === "") {
                this.addError(this.el.capacity, 'This field is required or Integer type is required');
                return false;
            }
            if (this.el.wtdate.value === "") {
                this.addError(this.el.wtdate, 'This field is required');
                return false;
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
                    _.bind(this.onUnknowError, this)
                );
            }, this);

            var onFinish = _.bind(function() {
                this.tip('Succeed!', 'success');
                utils.reload(500);
            }, this);

            var data = this.getData();

            if (this.el.pk.value !== "") {
                modifyTalk(data)
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            } else {
                addTalk(data)
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            }
        }
    }));

    $(function() {
        // FIXME
        TalkForm.tpl = _.template($("#form-tpl").html());

        var form = new TalkForm();
        var modal = new modals.FormModal();
        modal.setForm(form);
        $(modal.el).appendTo(document.body);

        $create = $("#create-talk");
        $create.click(function() {
            modal.show();
            modal.setTitle('Create Talk');
            modal.setSaveText("Create", "Creating...");
        });

        $("table").on("click", ".edit", function() {
            modal.setTitle('Edit Dialog');
            modal.setSaveText("Save ", "Saving...");
            var talk = $(this).parent().data();
            form.setTalk(talk);
            modal.show();
        });
    });

    $(function() {
        var modal = new modals.ActionModal();
        modal.setAction(function(id) {
            return deleteTalk(id).then(function() {
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
        modal.on('succeed', function() {
            utils.reload(500);
        });
        $("table").on("click", ".delete", function() {
            modal.setId($(this).parent().data('pk'));
            modal.show();
        });
    });
});
