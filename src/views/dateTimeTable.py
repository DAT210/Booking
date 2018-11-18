from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from src import app
from src.models import Restaurant
from src.templatebuild import buildSelectOptions
from src.templatebuild import buildTimesButtons
from flask import jsonify


dateTimeTable = Blueprint('dateTimeTable', __name__)

mail = Mail(app)


@dateTimeTable.route("/dateAndTime", methods=["POST"])
def dateAndTime():
    global selectedRestaurant
    restaurantID = request.form["theRestaurant"]
    selectedRestaurant=Restaurant.fetchRestaurant(restaurantID)
    return render_template('dateTimeTable/dateTime.html', restaurant=selectedRestaurant,restaurantID=restaurantID)

@dateTimeTable.route("/dateAndTime/date", methods=["POST"])
def dateAndTimePeople():
    global people
    people = request.form["people"]
    now = datetime.now()
    weeks=calculCalendarWeeks(now)
    numbers=dayNumberCalendar(now)
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT * FROM period";
    mycursor.execute(query)
    periods=mycursor.fetchall()
    periodsOptions=buildSelectOptions(periods)
    calendarOptions=buildSelectOptions(weeks)
    #Default fullDay
    mycursor.execute("INSERT INTO booking_info VALUES(30,1,'01'),(31,2,'02'),(32,3,'03'),(33,3,'04'),(34,4,'05'),(35,5,'05')")
    app.config["DATABASE"].commit()
    mycursor.execute("INSERT INTO rest_book VALUES(1,30,'01','2018-11-17',1),(1,31,'02','2018-11-17',1),(1,32,'03','2018-11-17',1),(1,33,'04','2018-11-17',1),(1,34,'05','2018-11-17',1)")
    app.config["DATABASE"].commit()
    fullDays=daysDisabled(now,periods[0][0])
    mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers,fullDays=fullDays)
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%Y-%m-%d")}
    return jsonify(response)



@dateTimeTable.route('/dateAndTime/time', methods=["POST"])
def times():
    period=request.form["period"]
    global dateSelected
    dateSelected=request.form["dateSelected"]
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

@dateTimeTable.route('/dateAndTime/tableVisualisation', methods=["POST"])
def chooseTableSelection():
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


@dateTimeTable.route('/dateAndTime/checkBooking', methods=["POST"])
def dateAndTimeCheck():
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]
    theRestaurant = selectedRestaurant.name
    theAddress = selectedRestaurant.street + ' , ' + str(selectedRestaurant.zip)
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime
    
    if (theEmail != ''):
        send_mail(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime)

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
    query="SELECT time_period.timeid FROM time_period WHERE period='"+str(period)+"';"
    mycursor.execute(query)
    times=mycursor.fetchall()
    timesList=""
    for time in times:
        timesList+=str(time[0])+","
    timesList=timesList[:-1]
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


