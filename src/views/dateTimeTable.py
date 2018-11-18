from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from datetime import datetime
from src import app
from src.models import Restaurant
from src.db_methods import db_get_periods, db_get_times, db_get_new_cid, db_get_timeid, db_insert_booking, db_insert_full_day, db_delete_full_day, db_get_times_from_period, db_get_unavailable_tables
from src.templatebuild import buildSelectOptions
from src.templatebuild import buildTimesButtons
from flask import jsonify


dateTimeTable = Blueprint('dateTimeTable', __name__)

mail = Mail(app)


@dateTimeTable.route("/dateAndTime/step_1", methods=["POST"])
def dateAndTime():
    global selectedRestaurant
    restaurantID = request.form["theRestaurant"]
    selectedRestaurant=Restaurant.fetchRestaurant(restaurantID)
    return render_template('dateTimeTable/dateTime.html', restaurant=selectedRestaurant,restaurantID=restaurantID)

@dateTimeTable.route("/dateAndTime/step_2", methods=["POST"])
def dateAndTimePeople():
    global people
    people = request.form["people"]
    now = datetime.now()
    weeks=calculCalendarWeeks(now)
    numbers=dayNumberCalendar(now)
    # from db_methods
    periods = db_get_periods()

    periodsOptions=buildSelectOptions(periods)
    calendarOptions=buildSelectOptions(weeks)
    # from db_methods
    db_insert_full_day()
    fullDays=daysDisabled(now,periods[0][0])
    db_delete_full_day()
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers,fullDays=fullDays)
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%Y-%m-%d")}
    return jsonify(response)



@dateTimeTable.route('/dateAndTime/step_3', methods=["POST"])
def times():
    period=request.form["period"]
    global dateSelected
    dateSelected=request.form["dateSelected"]
    # from db_methods
    times = db_get_times(period)
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT timeid,TIME_FORMAT(time,'%H:%i') FROM time_period WHERE period='"+str(period)+"';"
    mycursor.execute(query)
    times=mycursor.fetchall()
    mycursor.execute("INSERT INTO booking_info VALUES(30,1,'01'),(31,2,'02'),(32,3,'03'),(33,3,'04'),(34,4,'05'),(35,5,'05')")
    app.config["DATABASE"].commit()
    mycursor.execute("INSERT INTO rest_book VALUES(1,30,'01','2018-11-18',5),(1,31,'02','2018-11-18',5),(1,32,'03','2018-11-18',5),(1,33,'04','2018-11-18',5),(1,34,'05','2018-11-18',5)")
    app.config["DATABASE"].commit()
    fullTimes=timeDisabled(dateSelected,times,period)
    #Remove defaul fullDay
    mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    timesButton=buildTimesButtons(times,fullTimes=fullTimes)
    return render_template("dateTimeTable/time.html", times=timesButton)

@dateTimeTable.route('/dateAndTime/step_4', methods=["POST"])
def showButtons():
    global selectedTime
    selectedTime=request.form["selectedTime"]
    return render_template("dateTimeTable/buttonsTable.html",restaurant=Restaurant)

@dateTimeTable.route('/dateAndTime/changeCalendar', methods=["POST"])
def changeCalendar():
    now=datetime.now()
    beginDate=request.form["beginDate"]
    numbers=dayNumberCalendar(datetime.strptime(beginDate, '%d-%m-%Y'))
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers)
    response={"calendar" : templateCalendar,"currentDay":now.strftime("%d/%m/%Y")}
    return jsonify(response)

@dateTimeTable.route('/dateAndTime/step_5', methods=["POST"])
def unavailableTables():
    unvTables = db_get_unavailable_tables(selectedRestaurant.rid,selectedTime, dateSelected)
    return jsonify(tables=unvTables, nrOfPeople=people)

@dateTimeTable.route('/dateAndTime/step_6', methods=["POST"])
def bookedTables():
    global bookedTables
    bookedTables = request.json()
    return render_template("dateAndTime/formCheck.html", restaurant=Restaurant)

@dateTimeTable.route('/dateAndTime/step_7', methods=["POST"])
def dateAndTimeCheck():
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]
    theRestaurant = selectedRestaurant.name
    theRid = selectedRestaurant.rid
    theAddress = selectedRestaurant.street + ' , ' + str(selectedRestaurant.zip)
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime
    
    if (theEmail != ''): #if we confirm booking
        send_mail(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime)
        store_booking(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime,theRid)

    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime,
    theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)

def send_mail(name,email,restaurant,address,date,people,time):
    subject = 'Confirmation of booking - 45610'
    message = 'Hello '+name+', <br> <br>You have booked a table for '+people+' people at : <br>'+restaurant+'<br>'+address+'<br>'+date+' - '+time+' <br> To edit your reservation, click on the link below <br> http://localhost:5000 <br> Best regards, <br> <br>' + restaurant
    msg = Message(
        subject=subject,
        recipients=[email], 
        html=message
    )
    mail.send(msg)  

def store_booking(theName,theEmail,theAddress,theDate,theTime,theRid):
    date = datetime.strptime(theDate, '%d/%M/%Y')
    date = datetime.date(date)
    cid = db_get_new_cid()  # this should be from the customer guys (theName, theEmail, theAddress) ->
    timeid = db_get_timeid(theTime)

    db_insert_booking(theRid, 0, date, timeid, cid, "null")   # define tid (tableID) as 0 for the moment, also add_info is null atm


def calculCalendarWeeks(currentDate):
    weeks=[]
    beginCalendar = currentDate - timedelta(days=currentDate.weekday())
    for i in range(0,3):
        endCalendar = beginCalendar + timedelta(days=13)
        weeks+=[[beginCalendar.strftime("%d-%m-%Y"),beginCalendar.strftime("%d/%m")+" - "+endCalendar.strftime("%d/%m")]]
        beginCalendar=endCalendar+timedelta(days=1)

    return weeks

def dayNumberCalendar(currentDate):
    numbers=[]
    beginCalendar = currentDate - timedelta(days=currentDate.weekday())
    for i in range(0,14):
        number=(beginCalendar+timedelta(days=i))
        numbers+=[number]
    return numbers

def isDayDisabled(listTable,day,period):
    tablesNumber=len(listTable)
    listTable=','.join(listTable)
    mycursor=app.config["DATABASE"].cursor()

    # from db_methods
    times = db_get_times_from_period(period)
    timesList=""
    for time in times:
        timesList+=str(time[0])+","
    timesList=timesList[:-1]

    # not added in db_methods yet
    query="SELECT DISTINCT rest_book.tid FROM rest_book WHERE rest_book.tid IN("+str(listTable)+") and  rest_book.date='"+day+"' and rest_book.timeid IN("+timesList+")";
    mycursor.execute(query)
    tableBooked=mycursor.fetchall()

    return len(tableBooked)==tablesNumber

def daysDisabled(currentDate,period):
    listTable=["01","02","03","04","05"]
    daysDisabled=[]
    beginCalendar = currentDate - timedelta(days=currentDate.weekday())
    for i in range(0,14):
        disabled=isDayDisabled(listTable,(beginCalendar+timedelta(days=i)).strftime("%Y-%m-%d"),period)
        daysDisabled+=[disabled]
    return daysDisabled

def isTimeDisabled(selectedDate,time,period):
    listTable=["01","02","03","04","05"]
    tablesNumber=len(listTable)
    listTable=','.join(listTable)
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT DISTINCT rest_book.tid FROM rest_book JOIN time_period  on rest_book.timeid=time_period.timeid WHERE rest_book.tid IN("+str(listTable)+") AND time_period.period LIKE '"+period+"' AND rest_book.date='"+selectedDate+"' and rest_book.timeid BETWEEN "+str(time[0]-3)+" AND "+str(time[0]+3)+";"
    mycursor.execute(query)
    times=mycursor.fetchall()
    return len(times)==tablesNumber

def timeDisabled(selectedDate,times,period):
    listTable=["01","02","03","04","05"]
    timesDisabled=[]
    for time in times:
        disabled=isTimeDisabled(selectedDate,time,period)
        timesDisabled+=[disabled]
    return timesDisabled


