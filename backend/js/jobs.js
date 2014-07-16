define(function(require) {
    require("jquery");
    require("jquery.serializeObject");
    require("jquery.iframe-transport");
    require("bootstrap");
    require("select2")
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
    var formValidationProto = require("formValidationProto");
    var SimpleUpload = require("simple-upload");

    function modifyJobs(data) {
        var request = $.post("/backend/jobs/" + data.pk, data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function addJobs(data) {
        var request = $.post("/backend/jobs/add", data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function deleteJobs(id) {
        var request = $.post("/backend/jobs/delete", {
            id: id
        }, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function getUrl(key) {
        return "/backend/upload/" + key;
    }
    var proto = _.extend({}, formProto, formValidationProto);
    var PageForm = Backbone.View.extend(_.extend(proto, {
        initialize: function() {
            this.setElement($(PageForm.tpl())[0]);
            $(this.el).parsley({
                messages:{
                    required : "这是必填项。"
                }
            });
            $(this.el['place']).select2({
                formatNoMatches: function () { return "没有找到相关信息"; },
            });
            $(this.el['examplace']).select2({
                formatNoMatches: function () { return "没有找到相关信息"; },
            });
            $(this.el['type']).select2({
                formatNoMatches: function () { return "没有找到相关信息"; },
            });
            $(this.el['education']).select2({
                formatNoMatches: function () { return "没有找到相关信息"; },
            });
            this.$alert = this.$("p.alert");
            $("#id-ignore-number").change(function(){
            if($(this).is(":checked")){    
                $("#number").val('').hide();  
                $("#id_number").val('');
                this.el['number'].value = ''; 
            } else {
                $("#number").show();
            }   
            }); 
        },

        setPage: function(page) {
            _.each(['pk', 'name' , 'judge', 'place' ,'type', 'education', 'examplace','number','workdesc','jobdesc', 'condition'], _.bind(function(attr) {
                if(attr=='judge') {
                    this.el[attr].checked = page[attr];
                }
                else if(attr=='place'||attr=='type'||attr=='education'||attr=='examplace'){
                    $(this.el[attr]).select2('val',page[attr]);
                }
                else if(attr=='number'){
                    this.el[attr].value = page[attr];
                    numbers = page[attr];
                    if(numbers != 0){
                        $("#id-ignore-number").prop('checked',false);
                        $("#number").show();  
                    } else {
                        $("#id-ignore-number").prop('checked',true);
                        $("#number").hide(); 
                        this.el[attr].value = null;   
                        $("#id_number").val('');
                    }
                }
                else{
                    this.el[attr].value = page[attr];
                }

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
                if(attr=='judge'){
                    this.el[attr].checked = false;
                }
                if(attr=='place'||attr=='examplace'){
                    $(this.el[attr]).select2('val','');
                }
                if(attr=='type')
                    $(this.el[attr]).select2('val','TE');
                if(attr=='education')
                    $(this.el[attr]).select2('val','QT');
                if(attr=='number'){
                    $("#id-ignore-number").prop('checked',true);                     
                    $("#number").hide();    
                }
            }, this));
            this.clearErrors(['number']);
            this.clearTip();
            $(this.el).parsley('destroy');
        },
        validate: function() {            
            this.clearErrors(['number']);
            judge = this.el['number'].value;
            if(this.$("#id-ignore-number").is(":checked")){
                this.el['number'].value = 0;
            }else{
                if(judge === ""|| parseInt(judge)!=judge){
                    this.addError(this.el.number, '这是必填项/必须填入整数。');
                    return false;
                }
                if(judge <=0){
                    this.addError(this.el.number, '请填入一个正数。');
                    return false;
                }
                if(judge >1000000){
                    this.addError(this.el.number, '请填入合适的正数。');
                    return false;
                }
            }
            return true;
        },
        save: function() {
            var onComplete = _.bind(function() {
                this.trigger('save');
            }, this);
            
            if (!this.validate()){
                return setTimeout(onComplete,0);    
            }
            
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
                this.tip('成功!', 'success');
                utils.reload(500);
            }, this);

            if (this.el.pk.value !== "") {
                modifyJobs(this.$el.serializeObject())
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            } else {
                addJobs(this.$el.serializeObject())
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            }
        }
    }));

    $(function() {

        PageForm.tpl = _.template($("#form_tpl").html());
      
        var form = new PageForm();
        var modal = new modals.FormModal();
        modal.setForm(form);

        $(modal.el).appendTo(document.body);

        $create = $("#create-page");
        $create.click(function() {
            modal.show();
            modal.setTitle('创建招聘信息');
            modal.setSaveText("创建", "创建中...");
        });


        $("table").on("click", ".edit", function() {
            modal.setTitle('编辑招聘信息');
            modal.setSaveText("保存", "保存中...");
            var page = $(this).parent().data();
            form.setPage(page);
            modal.show();
        });
    });

    $(function() {
        $("#id-ignore-number").change(function(){
            if($(this).is(":checked")){    
                $("#number").val('').hide();  
                $("#id_number").val('');
                this.el['number'].value = ''; 
            } else {
                $("#number").show();
            }   
        });      
        var modal = new modals.ActionModal();
        modal.setAction(function(id) {
            return deleteJobs(id).then(function() {
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
