define(function(require) {
    require("jquery");
    require("bootstrap-datetimepicker");
    require("zh-CN");
    require("moment");

    $(function(){
        $form = $("form.form-inline");
        form = $form[0];
        $(form.start).datetimepicker({
            maxView: 2,
            minView: 2,
            format: 'yyyy-mm-dd',
            autoclose: "true",
            language: 'zh-CN',
        });
        $(form.stop).datetimepicker({
            maxView: 2,
            minView: 2,
            format: 'yyyy-mm-dd',
            autoclose: "true",
            language: 'zh-CN',
        });

        function onFilterChange() {
            if(!$("#alert").hasClass("hidden")){
                if($(form.start).val() <= $(form.stop).val()){
                    $("#alert").addClass("hidden");
                    $(form).submit();
                }
            }else{
                if($(form.start).val() > $(form.stop).val()){
                    $("#alert").removeClass("hidden");
                }else{
                    $(form).submit();
            }}
        }
        $(form.start).datetimepicker('setEndDate', moment().format("YYYY-MM-DD"));
        $(form.stop).datetimepicker('setEndDate', moment().format("YYYY-MM-DD"));

        $(form.start).change(onFilterChange);
        $(form.stop).change(onFilterChange);
    });
});

