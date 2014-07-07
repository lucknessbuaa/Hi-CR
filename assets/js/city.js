$(".modal-dialog").load(function() {
    var city = document.getElementById("id_city");
    var university = document.getElementById("id_university");
    
    len = university.options.length;
    for(var i = 0; i < len; i ++){
        university.options[i] = null;
    }
    function removeOptions(selectObj) {
        var len = selectObj.options.length;
        for (var i = 0; i < len; i++) {
            selectObj.options[i] = null;
        }
    }

    function setUniversity() {
        if (city.value == "") {} else {
            var cityS = city.value;
            if (cityS == "1") {
                removeOptions(university);
                var start = 0;
                university.options[0] = new Option("-----", '');
                start++;

                university.option[1] = new Option("beiahng", "beihang");

            }

        }
    }
    //city.onchange = setUniversity;


});
