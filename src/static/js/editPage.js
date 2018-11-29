$(document).ready(function(){

    $("#formNumberPeopleEdit").submit(function(event)
    {
        var name=$("#nameEdit").val();
        var phone=$("#phoneEdit").val();
        var email=$("#emailEdit").val();
        event.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#updatePage").html(this.responseText);
                $(".cp-spinner").remove();
                $("#selectNumberPeopleEdit").change(function(e){
                    var xhttp = new XMLHttpRequest();
                    $("#restaurantInfo").remove();
                    xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        $("#peopleColumn").remove();
                        var response= JSON.parse(this.responseText);
                        $("#updatePage").append(response["calendar"]);
                        $("#buttonsCalendar").append(response["buttonsCalendar"]);
                        disableCalendarDays(response["currentDay"]);
                        $(".cp-spinner").remove();
                        $(".calendarItem:not(.disabled)").on("click",function(e){
                            selectDay(e,this);
                        });
                        $("#selectDate").on("change",function(e){
                            changeCalendar(e,this);
                        });
                        console.log(response["people"])
                        $("#peopleInfo").val(response["people"]);
                        $("#bookingInfo").show();
                    }
                    };
                    xhttp.open("POST", "/editPage/UpdateDateEdit");
                    var data=$(this).val();
                    var formData="people="+data;
                    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhttp.send(formData);
                });
            }
        };
        xhttp.open("POST", "/editPage/UpdatenumberPeople");
        var formData=$(this).serialize();
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        xhttp.send(formData);
    })

   

    $("#formDateEdit").submit(function(e)
    {   
        e.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#updatePage").html("");
                var response= JSON.parse(this.responseText);
                $("#updatePage").append(response["calendar"]);
                $("#buttonsCalendar").append(response["buttonsCalendar"]);
                disableCalendarDays(response["currentDay"]);
                $(".cp-spinner").remove();
                $("#peopleInfo").val(response["people"]);
                $(".calendarItem:not(.disabled)").on("click",function(e){
                    selectDay(e,this);
                });
                $("#selectDate").on("change",function(e){
                    changeCalendar(e,this);
                });
                $("#bookingInfo").show();
            }
        };
        xhttp.open("POST", "/editPage/UpdateDateEdit");
        var data=$("#numberPeople").val();
        var formData="people="+data;
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(formData);
    });

    $("#formTimeEdit").submit(function(e)
    {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $(".cp-spinner").remove();
                $("#updatePage").html(this.responseText);
                $(".btnTime").on("click",function(e){
                    selectTime(e,this);
                });
            }
        };
        xhttp.open("POST", "/editPage/UpdatetimeEdit");
        var data=$("#selectPeriod").val();
        var formData="period="+data+"&dateSelected="+day;
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(formData);
    });


    function selectDay(e,itemClicked)
    {

        var day=$(itemClicked).children().first().children("a").data("dateday");
        console.log(day);
        e.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#bookingCalendar").remove();
                console.log(this.responseText);
                $("#restaurantInfo").parent().append(this.responseText);
                $(".cp-spinner").remove();
                $("#bookingInfo .card-body").append("<div class=\"form-group\">" +
                    "<label class=\"form-label\" for=\"dateInfo\">Booking date</label>" +
                    "<input name=\"dateInfo\" id=\"dateInfo\" disabled=\"\" class=\"form-control\">" +
                    "</div>");
                $("#dateInfo").val(day);
                $("#selectDate").remove();
                $("#selectPeriod").remove();
                $(".btnTime").on("click",function(e){
                    selectTime(e,this);
                });
            }
        };
        xhttp.open("POST", "/dateAndTime/time");
        var data=$("#selectPeriod").val();
        var formData="period="+data+"&dateSelected="+day;
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(formData);
    };

    $("#formConfirmBooking").submit(function(event)
    {
        event.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#updatePage").html(this.responseText);
                $("#bookingInfo").show();
                $(".cp-spinner").remove();
            }
        };
        xhttp.open("POST", "/editPage/checkBookingEdit");
        var formData=$(this).serialize();
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        xhttp.send(formData);
    })

    function checkBooking(event)
    {
        event.preventDefault();
        console.log("fuck");
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log("fucks");
                $("#updatePage").html(this.responseText);
                $("#bookingInfo").show();
                $(".cp-spinner").remove();
            }
        };
        xhttp.open("POST", "/editPage/checkBookingEdit");
        var formData=$("#formCheckEdit").serialize();
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        xhttp.send(formData);
    }
    function selectTime(e,itemClicked)
    {
        var name=$("#nameEdit").text();
        var phone=$("#phoneEdit").text();
        var email=$("#emailEdit").text();
        console.log(email);
        var time=$(itemClicked).text();
        console.log(time);
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#timeColumn").remove();
                $("#restaurantInfo").parent().append(this.responseText);
                $(".cp-spinner").remove();
                $("#bookingInfo .card-body").append("<div class=\"form-group\">" +
                    "<label class=\"form-label\" for=\"timeInfo\">Booking time</label>" +
                    "<input name=\"timeInfo\" id=\"timeInfo\" disabled=\"\" class=\"form-control\">" +
                    "</div>");
                $("#timeInfo").val(time);
                $("#formConfirmBooking").submit(function(event)
                {
                    event.preventDefault();
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            $("#updatePage").html(this.responseText);
                            $("#bookingInfo").show();
                            $(".cp-spinner").remove();
                        }
                    };
                    xhttp.open("POST", "/editPage/checkBookingEdit");
                    var formData=$(this).serialize();
                    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
                    xhttp.send(formData);
                })
            }
        };
        xhttp.open("POST", "/editPage/tableVisualisationEdit");
        var formData="selectedTime="+time+"&theName="+name+"&thePhone="+phone+"&theEmail="+email;
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(formData);
    }
    function disableCalendarDays(activeDate)
    {
        var dayNumbers=$(".dayNumber a");
        var activeDateFound=false;
        var i=0;
        var lengthCalendar=dayNumbers.length;
        activeDate=activeDate.split("/");
        activeDate=new Date(activeDate[2],activeDate[1],activeDate[0]);
        while(i<lengthCalendar && !activeDateFound)
        {
            var date=$(dayNumbers[i]).data("dateday").split("/");
            date=new Date(date[2],date[1],date[0]);
            if(date>=activeDate)
                activeDateFound=true;
            else
            {
                $(dayNumbers[i]).parent().parent().addClass("disabled");
                i++;
            }
        }
    }
    function changeCalendar(e,itemClicked)
    {

        var beginDate=$(itemClicked).val();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#bookingCalendar").remove();
                var response= JSON.parse(this.responseText);
                $("#restaurantInfo").parent().append(response["calendar"]);
                $(".cp-spinner").remove();
                disableCalendarDays(response["currentDay"]);
                $(".calendarItem:not(.disabled)").on("click",function(e){
                    selectDay(e,this);
                });
            }
        };
        xhttp.open("POST", "/dateAndTime/changeCalendar");
        var formData="beginDate="+beginDate;
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(formData);
    }

});

    // $("#EditBooking").submit(function(event)
    // {
    //     event.preventDefault();
    //     var xhttp = new XMLHttpRequest();
    //     xhttp.onreadystatechange = function() {
    //         if (this.readyState == 4 && this.status == 200) {
    //             $("#main").html(this.responseText);
    //             $(".cp-spinner").remove();
    //         }
    //     };
    //     xhttp.open("POST", "/dateAndTime/removeBooking");
    //     var formData=$(this).serialize();
    //     xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    //     xhttp.send(formData);
    // })

    // $("#DeltedBooking").submit(function(event)
    // {
    //     event.preventDefault();
    //     var xhttp = new XMLHttpRequest();
    //     xhttp.onreadystatechange = function() {
    //         if (this.readyState == 4 && this.status == 200) {
    //             $("#main").html(this.responseText);
    //             $(".cp-spinner").remove();
    //         }
    //     };
    //     xhttp.open("POST", "/dateAndTime/removeBooking");
    //     var formData=$(this).serialize();
    //     xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    //     xhttp.send(formData);
    // })
