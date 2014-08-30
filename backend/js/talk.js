define(function(require) {
    require("jquery");
    require("jquery.serializeObject");
    require("jquery.iframe-transport");
    require("bootstrap");
    require("moment");
    require("bootstrap-datetimepicker");
    require("zh-CN");
    require("select2");
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
            this.$("[name=place]").attr({
                maxlength: 100
            });
            this.$("[name=speaker]").attr({
                maxlength: 50
            });

            this.$("#number").change(_.bind(this.ensureNumber, this));
            $(this.el.grabbing).click(_.bind(this.ensureSeats, this));
            this.ensureNumber();

            this.$("[name=wtdate]").click(function() {
                var time = document.getElementById('id_date').value || moment();
                $(document.getElementById('id_wtdate')).val(moment(time, "YYYY-MM-DD HH:mm").format("YYYY-MM-DD HH:mm")).trigger('change');
                $(document.getElementById('id_wtdate')).datetimepicker('setStartDate', moment(time, "YYYY-MM-DD HH:mm").format("YYYY-MM-DD HH:mm"));
            });
        },

        ensureNumber: function() {
            if (this.$("#number").prop("checked")) {
                $(this.el.grabbing).prop("checked", false).attr('disabled', 'disabled');
            } else {
                $(this.el.grabbing).removeAttr('disabled');
            }

            this.ensureSeats();
        },

        ensureSeats: function() {
            if ($(this.el.grabbing).prop("checked")) {
                this.$el.find(".seats").show();
            } else {
                this.$el.find(".seats").hide();
                this.el.seats.value = "";
            }
        },

        events: {
            'change [name=city]': 'onCityChanged',
            'change [name=number]': 'onCapacityChanged',
        },

        onCapacityChanged: function() {
            if (this.$("#number").is(":checked")) {
                this.$(".group-capacity").addClass("hide");
                this.el['capacity'].value = '';
            } else {
                this.$(".group-capacity").removeClass("hide");
            }
        },

        setCapacity: function() {
            if (this.el.capacity.value > 0) {
                this.$("#number").prop({
                    "checked": false
                });
                this.$(".group-capacity").removeClass("hide");
            } else {
                this.$("#number").prop({
                    checked: "checked"
                });
                this.$(".group-capacity").addClass("hide");
            }
        },

        setDate: function() {
            this.$("[name=wtdate]").attr({
                readOnly: "true"
            });
            this.$("[name=date]").attr({
                readOnly: "true"
            });
            this.$("[name=date]").datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
            });
            this.$("[name=wtdate]").datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
            });

            this.$("[name=date]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
            this.$("[name=wtdate]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        },

        setTalk: function(talk) {
            _.each(['pk', 'city', 'university', 'date', 'place', 'capacity', 'speaker', 'wtdate', 'seats'], _.bind(function(attr) {
                this.el[attr].value = talk[attr];
            }, this));

            $(this.el.grabbing).prop('checked', talk.grabbing);

            if (this.el['capacity'].value == 0) {
                this.el['capacity'].value = '';
            }
            this.setCapacity();

            this.ensureNumber();
        },

        bind: function(data) {
            var defaults = {
                id: '',
                title: '',
                description: '',
                url: ''
            };
            data = _.defaults(data, defaults);
            _.each(['pk', 'city', 'university', 'date', 'place', 'capacity', 'speaker', 'wtdate', 'seats', 'grabbing'], _.bind(function(attr) {
                this.el[attr].value = data[attr];
            }, this));
        },

        initCU: function() {
            this.$("[name=city]").select2({
                data: selectCity,
                formatNoMatches: '没有相关信息',
                initSelection: function(element, callback) {
                    if (element.val() == "") {
                        var data = {
                            id: selectCity[0].id,
                            text: selectCity[0].name
                        };
                    } else {
                        for (var i = 0; i < selectCity.length; i++) {
                            if (selectCity[i].id == element.val()) {
                                var data = {
                                    id: element.val(),
                                    text: selectCity[i].name
                                };
                                break;
                            }
                        }
                    }
                    callback(data);
                }
            });
            this.$("[name=university]").select2({
                query: function(query) {
                    var uni = {
                        results: []
                    };
                    if (document.getElementById('id_city').value === "") {
                        document.getElementById('id_city').value = '1';
                    }
                    for (var i = 0; i < selectUni.length; i++) {
                        if (selectUni[i].city == document.getElementById('id_city').value && (selectUni[i].name.indexOf(query.term) != -1)) {
                            uni.results.push(selectUni[i]);
                        }
                    }
                    query.callback(uni);
                },


                initSelection: function(element, callback) {
                    if (element.val() == "") {
                        var data = {
                            id: selectUni[0].id,
                            text: selectUni[0].name
                        };
                    } else {
                        for (var i = 0; i < selectUni.length; i++) {
                            if (selectUni[i].id == element.val()) {
                                var data = {
                                    id: element.val(),
                                    text: selectUni[i].name
                                };
                                break;
                            }
                        }
                    }
                    callback(data);
                },

                formatNoMatches: function(term) {
                    return '没有相关信息';
                }
            });
        },

        onCityChanged: function() {
            for (var i = 0; i < selectUni.length; i++) {
                if (selectUni[i].city == document.getElementById('id_city').value) {
                    var data = selectUni[i];
                    break;
                }
            }
            this.$("[name=university]").select2('data', data);
        },

        onShow: function() {
            this.initCU();
            this.setDate();
        },

        clear: function() {
            _.each(['pk', 'city', 'university', 'date', 'place', 'clear', 'capacity', 'speaker', 'wtdate', 'seats'], _.bind(function(field) {
                $(this.el[field]).val('');
            }, this));

            $(this.el.grabbing).prop('checked', false);
            $('[name=cover]').val("").trigger('change');
            this.setCapacity();
            this.clearTip();
            this.ensureNumber();
        },

        onHide: function() {
            this.clear();
            this.clearErrors(['city', 'university', 'date', 'place', 'cover', 'capacity', 'speaker', 'wtdate'])
            $(this.el).parsley('destroy');
        },

        getData: function() {
            var data = _.defaults(this.$el.serializeObject(), {
                grabbing: false,
                seats: 0
            });
            data.seats = data.seats || 0;
            data['place'] = data['place'].trim();
            data['speaker'] = data['speaker'].trim();

            return data;
        },

        validate: function() {
            this.clearErrors(['city', 'university', 'date', 'place', 'cover', 'capacity', 'speaker', 'wtdate', 'seats', 'grabbing']);
            this.clearTip();

            if (this.el.city.value === "") {
                this.el.city.value = '1';
            }
            if (this.el.university.value === "") {
                this.el.university.value = '1';
            }
            if (this.el.date.value === "") {
                this.addError(this.el.date, '这是必填项。');
                return false;
            }
            if (this.el.place.value.trim() === "") {
                this.addError(this.el.place, '这是必填项。');
                return false;
            }
            if (this.el.cover.value.trim() === "") {
                this.addError(this.el.cover, '这是必填项。');
                return false;
            }
            capa = this.el.capacity.value;
            if (this.$("#number").is(":checked")) {
                this.el.capacity.value = 0;
            } else {
                if (capa === "" || parseInt(capa) != capa) {
                    this.addError(this.el.capacity, '这是必填项/应该填入整数。');
                    return false;
                }
                if (capa <= 0) {
                    this.addError(this.el.capacity, '必须输入正数。');
                    return false;
                }
                if (capa >= 2000) {
                    this.addError(this.el.capacity, '座位数应该小于2000！');
                    return false;
                }
            }

            if (!this.$("#number").prop("checked") && $(this.el.grabbing).prop("checked")) {
                var seats = this.el.seats.value;
                if (seats !== "") {
                    if (!/^\d+$/.test(seats)) {
                        this.addError(this.el.seats, '这是必填项/应该填入整数。');
                        return false;
                    }

                    seats = parseInt(seats);
                    if (seats > capa) {
                        this.addError(this.el.seats, '占座数量不应该超过总座位数量');
                        return false;
                    }
                }
            }

            if (this.el.wtdate.value === "") {
                this.addError(this.el.wtdate, '这是必填项。');
                return false;
            }
            if (this.el.wtdate.value <= this.el.date.value) {
                this.addError(this.el.wtdate, '笔试时间应该在宣讲会时间之后。');
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
                    _.bind(this.onUnknownError, this)
                );
            }, this);

            var onFinish = _.bind(function() {
                this.tip('成功！', 'success');
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
        TalkForm.tpl = _.template($("#form-tpl").html());

        var form = new TalkForm();
        var modal = new modals.FormModal();
        modal.setForm(form);
        $(modal.el).appendTo(document.body);

        $create = $("#create-talk");
        $create.click(function() {
            modal.show();
            modal.setTitle('创建宣讲会信息');
            modal.setSaveText("创建", "创建中...");
        });

        var hello = new AjaxUploadWidget($('[name=cover]'), {
            changeButtonText: "修改图片",
            removeButtonText: "删除图片",
            onError: function(data) {
                toast('error', '图片上传失败，请重试。');
            }
        });

        $("table").on("click", ".edit", function() {
            modal.setTitle('编辑宣讲会信息');
            modal.setSaveText("保存", "保存中...");
            var talk = $(this).parent().data();
            $('[name=cover]').val(talk.cover).trigger('change');
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
        modal.setTitle('删除宣讲会信息');
        modal.tip('确定要删除吗？');
        modal.setSaveText('删除', '删除中...');
        modal.on('succeed', function() {
            utils.reload(500);
        });
        $("table").on("click", ".delete", function() {
            modal.setId($(this).parent().data('pk'));
            modal.show();
        });
    });

});
