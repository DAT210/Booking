$(document).ready(function(){

    $("label").on({
        mouseenter: function(){
            var className = this.className;
            var changeThis = "#opening_hours" + className[className.length - 1];
            console.log(changeThis)
            $(changeThis).show();
        },
        mouseleave: function(){
            var className = this.className;
            var checkThis = ".radio" + className[className.length - 1];
            if ($(checkThis).is(":checked")){
                return
            }
            var changeThis = "#opening_hours" + className[className.length - 1];
            $(changeThis).hide();
        }
    });

    $("input[type=radio]").change(function(){
        var className = this.className;
        var changeThis = "#opening_hours" + className[className.length - 1];

        $(".opnhrs").each(function(){
            $(this).hide();
        });

        $(changeThis).show();


    });

    $("#formSearchRestaurant").submit(function(event)
    {
        event.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#main").html(this.responseText);
                $(".cp-spinner").remove();
            }
        };
        xhttp.open("POST", "/dateAndTime/step_1");
        var formData=$(this).serialize();
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        xhttp.send(formData);
    })
});