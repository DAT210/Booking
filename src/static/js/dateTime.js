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
                disableCalendarDays(response["currentDay"]);
                $(".cp-spinner").remove();
                $(".calendarItem:not(.disabled)").on("click",function(e){
                    selectDay(e,this);
                });
                $("#selectDate").on("change",function(e){
                    changeCalendar(e,this);
                });
                console.log(response["people"]);
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
    function selectDay(e,itemClicked)
    {

        var day=$(itemClicked).children().first().children("a").data("dateday");
        console.log(day);
        event.preventDefault();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#bookingCalendar").remove();
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
                $("#main").html(this.responseText);
                $("#bookingInfo").show();
                $(".cp-spinner").remove();
            }
        };
        xhttp.open("POST", "/dateAndTime/checkBooking");
        var formData=$(this).serialize();
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
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
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(formData);
    }
    function selectTime(e,itemClicked)
    {

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
                $("#chooseTable").on("click", function(){
                    $("#chooseTableVisualisation").remove();
                    tableVis();
                });
            }
        };
        xhttp.open("POST", "/dateAndTime/showButtons");
        var formData="selectedTime="+time;
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

    function tableVis(){ // first sends a ajax req to our own flask app to get values from db
                        // then sends a ajax req with the json that flask method made to tableVis
        // event.preventDefault();
        showTableVisualization($("#restaurantIdInfo").val());
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200){
                bookedTables = sendTableVisRequest(this.responseText);
                sendBookedTables(bookedTables);
                }
        };
        xhttp.open("POST", "/dateAndTime/unvtables");

        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send();
    }

    function sendTableVisRequest(dataJSON) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                return this.responseText;
            }
        };
        xhttp.open("POST", "/tableVisualization");   // ?their url
        var formData="data=" + dataJSON;
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(formData);
    }


    function showTableVisualization(restaurantName){
        var theUrl = "http://127.0.0.1:5000/";   // ? their url + /restaurantName
        var theFrame = $("<iframe></iframe>").attr({"id":"tableSelection","src": theUrl, "height": "350", "width": "600", "scrolling": "no"});
        $("#restaurantInfo").parent().append(theFrame);
    }

    function sendBookedTables(dataJSON) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                $("#restaurantInfo").parent().append(this.responseText);
                $("#checkBooking").on("click",function(e){
                    checkBooking(e);
                });
            }
        };
        xhttp.open("POST", "/dateTime/bookedTables");
        var formData = "data=" + dataJSON;
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(formData);
    }

});