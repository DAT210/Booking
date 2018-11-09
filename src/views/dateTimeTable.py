from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from src import app
from src.models import Restaurant
from src.templatebuild import buildSelectOptions
from src.templatebuild import buildTimesButtons
from flask import jsonify

dateTimeTable = Blueprint('dateTimeTable', __name__)


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
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers)
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%d/%m/%Y")}
    return jsonify(response)



@dateTimeTable.route('/dateAndTime/time', methods=["POST"])
def times():
    period=request.form["period"]
    global dateSelected
    dateSelected=request.form["dateSelected"]
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT TIME_FORMAT(time,'%H:%i') FROM time_period WHERE period='"+str(period)+"';"
    mycursor.execute(query)
    times=mycursor.fetchall()
    timesButton=buildTimesButtons(times)
    return render_template("dateTimeTable/time.html", times=timesButton)

@dateTimeTable.route('/dateAndTime/showButtons', methods=["POST"])
def showButtons():
    global selectedTime
    selectedTime=request.form["selectedTime"]
    return render_template("dateTimeTable/buttonsTable.html")

@dateTimeTable.route('/dateAndTime/bookedTables', methods=["POST"])
def bookedTables():
    global bookedTables
    bookedTables = request.json()
    return render_template("dateAndTime/formCheck.html", restaurant=Restaurant)

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
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime

    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime,
    theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)


@dateTimeTable.route('/dateAndTime/unvtables', methods=["POST"])
def unavailableTables():
    unvTables = db_get_unavailable_tables(selectedRestaurant,selectedTime, dateSelected)
    return jsonify(tables=unvTables, nrOfPeople=people)


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

def db_get_unavailable_tables(rid, time, date):
    timeid = db_get_corresponding_time_id(time)
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "SELECT tid FROM rest_book WHERE rid=%s AND timeid=%s AND date=%s"
        mycursor.execute(sql, (rid, timeid, date))
        unvTables = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()
    return unvTables

def db_get_corresponding_time_id(time):
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "SELECT timeid FROM time_period WHERE time=%s"
        mycursor.execute(sql, (time,))
        timeid = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()
    print(timeid)
    return timeid



