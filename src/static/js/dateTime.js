$(document).ready(function(){



    $("#selectNumberPeople").change(function(e)
    {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#peopleColumn").remove();
                var response= JSON.parse(this.responseText);
                $("#rowButton").append(response["buttonsCalendar"]);
                $("#restaurantInfo").parent().append(response["calendar"]);
                $(".cp-spinner").remove();
                $("#triggerTime").on("click",function(e){
                    triggerTime(e);
                });
                $("#checkBooking").on("click",function(e){
                    checkBooking(e);
                });
                console.log(response["people"])
                $("#peopleInfo").val(response["people"]);
                $("#bookingInfo").show();
            }
        };
        xhttp.open("POST", "/dateAndTime/date");
        var data=$(this).val();
        var formData="people="+data;
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(formData);
    });
    function triggerTime(e)
    {
        event.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#bookingCalendar").remove();
                $("#restaurantInfo").parent().append(this.responseText);
                $(".cp-spinner").remove();
                $("#triggerTime").remove();
            }
        };
        xhttp.open("POST", "/dateAndTime/time");
        var data=$("#selectPeriod").val();
        var formData="period="+data;
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(formData);
    };



    $("#formConfirmBooking").submit(function(event)
    {
        event.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#main").html(this.responseText);
                $("#bookingInfo").show();
                $(".cp-spinner").remove();
            }
        };
        xhttp.open("POST", "/dateAndTime/checkBooking");
        var formData=$(this).serialize();
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        xhttp.send(formData);
    })

    function checkBooking(event)
    {
        event.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#main").html(this.responseText);
                $("#bookingInfo").show();
                $(".cp-spinner").remove();
            }
        };
        xhttp.open("POST", "/dateAndTime/checkBooking");
        var formData=$("#formCheck").serialize();
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        xhttp.send(formData);
    }

});