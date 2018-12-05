from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from src import app
from src.models import Restaurant
from src.db_methods import db_get_periods, db_get_times,db_insert_full_day, db_delete_full_day, db_get_times_from_period,db_get_attendance
from src.templatebuild import buildSelectOptions
from src.templatebuild import buildTimesButtons
from flask import jsonify


dateTimeTable = Blueprint('dateTimeTable', __name__)



@dateTimeTable.route("/step_1/people", methods=["POST"])
def dateAndTime():
    restaurantID = request.form["theRestaurant"]
    selectedRestaurant=Restaurant.fetchRestaurant(restaurantID)
    return render_template('dateTimeTable/dateTime.html', restaurant=selectedRestaurant,restaurantID=restaurantID)

@dateTimeTable.route("/step_2/date", methods=["POST"])
def dateAndTimePeople():
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
    attendances=attendance(now,periods[0][0])
    db_delete_full_day()
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers,fullDays=fullDays,attendances=attendances)
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%Y-%m-%d"),"restaurantCapacity":50}
    return jsonify(response)



@dateTimeTable.route('/step_3/time', methods=["POST"])
def times():
    period=request.form["period"]
    dateSelected=request.form["dateSelected"]
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT timeid,TIME_FORMAT(time,'%H:%i') FROM time_period WHERE period='"+str(period)+"';"
    mycursor.execute(query)
    times=mycursor.fetchall()
    mycursor.execute("INSERT INTO booking_info VALUES(36,1,'01'),(37,2,'02'),(38,3,'03'),(39,3,'04'),(40,4,'05')")
    app.config["DATABASE"].commit()
    mycursor.execute("INSERT INTO rest_book VALUES(1,36,'01','2018-11-25',5,3),(1,37,'02','2018-11-25',5,2),(1,38,'03','2018-11-25',5,2),(1,39,'04','2018-11-25',5,2),(1,40,'05','2018-11-25',5,3)")
    app.config["DATABASE"].commit()
    fullTimes=timeDisabled(dateSelected,times,period)
    mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(36,37,38,39,40)")
    mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(36,37,38,39,40)")
    app.config["DATABASE"].commit()
    timesButton=buildTimesButtons(times,fullTimes=fullTimes)
    return render_template("dateTimeTable/time.html", times=timesButton)


@dateTimeTable.route('/changeCalendar', methods=["POST"])
def changeCalendar():
    now=datetime.now()
    beginDate=request.form["beginDate"]
    period=request.form["period"]
    numbers=dayNumberCalendar(datetime.strptime(beginDate, '%d-%m-%Y'))
    fullDays=daysDisabled(datetime.strptime(beginDate, '%d-%m-%Y'),period)
    attendances=attendance(datetime.strptime(beginDate, '%d-%m-%Y'),period)
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers,fullDays=fullDays,attendances=attendances)
    response={"calendar" : templateCalendar,"currentDay":now.strftime("%Y-%m-%d"),"restaurantCapacity":50}
    return jsonify(response)

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

def attendance(currentDate,period):

    beginCalendar = currentDate - timedelta(days=currentDate.weekday())
    attendance=[]
    for i in range(0,14):
        attendance+=[db_get_attendance((beginCalendar+timedelta(days=i)).strftime("%Y-%m-%d"),period)]
    return attendance

