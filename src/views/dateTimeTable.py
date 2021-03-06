from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from datetime import datetime
from src import app
import mysql.connector
from src.models import Restaurant
from src.db_methods import get_restaurantName, db_get_time, db_get_timeid, db_get_restBookInfo, db_get_customerInfo, db_get_periods, db_get_times,db_insert_full_day, db_delete_full_day, db_get_times_from_period,db_get_attendance
from src.templatebuild import buildSelectOptions
from src.templatebuild import buildTimesButtons
from flask import jsonify


dateTimeTable = Blueprint('dateTimeTable', __name__)



@dateTimeTable.route("/dateAndTime/step_1", methods=["POST"])
def dateAndTime():
    restaurantID = request.form["theRestaurant"]
    selectedRestaurant=Restaurant.fetchRestaurant(restaurantID)
    return render_template('dateTimeTable/dateTime.html', restaurant=selectedRestaurant,restaurantID=restaurantID)

@dateTimeTable.route("/dateAndTime/step_2", methods=["POST"])
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
    beginCalendar = now - timedelta(days=now.weekday())
    fullDays=daysDisabled(beginCalendar,periods[0][0])
    attendances=attendance(beginCalendar,periods[0][0])
    db_delete_full_day()
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers,fullDays=fullDays,attendances=attendances)
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%Y-%m-%d"),"restaurantCapacity":50}
    return jsonify(response)



@dateTimeTable.route('/dateAndTime/step_3', methods=["POST"])
def times():
    period=request.form["period"]
    dateSelected=request.form["dateSelected"]
    # from db_methods
    times = db_get_times(period)
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

@dateTimeTable.route('/editPage/tableVisualisationEdit/<bid>', methods=["POST"])
def chooseTableSelectionEdit(bid):
    global selectedTime
    selectedTime=request.form["selectedTime"]
    theName=request.form["theName"]
    thePhone=request.form["thePhone"]
    theEmail=request.form["theEmail"]
    theRestaurant=Restaurant.fetchRestaurant(request.form["theRestaurant"])
    return render_template("editPage/buttonsTableEdit.html",restaurant=theRestaurant,theName=theName,thePhone=thePhone,theEmail=theEmail,theBid=bid)

@dateTimeTable.route('/editPage/checkBookingEdit/<bid>', methods=["POST"])
def dateAndTimeCheckEdit(bid):
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]
    selectedRestaurant= Restaurant.fetchRestaurant(request.form["theRestaurant"])
    theAddress = selectedRestaurant.street + ' , ' + str(selectedRestaurant.zip)
    theDate = request.form["theDate"]
    thePeople = request.form["thePeople"]
    theTime=request.form["theTime"]
    # bid = request.form["theBid"]
    # date = theDate.strftime('%Y-%m-%d')
    timeid = db_get_timeid(theTime)

    update_rest_book(bid, theDate, timeid, thePeople)

    return render_template("editPage/confirmDateEdit.html", theDate=theDate, theTime=theTime,
                           theRestaurant=selectedRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail,theBid=bid)


def update_rest_book(bid, theDate, timeid, thePeople):
    conn = app.config["DATABASE"]
    mycursor=conn.cursor()
    try:
        pass
        query =  "UPDATE rest_book SET date = %s, timeid = %s, people = %s WHERE bid = %s"
        print(theDate)
        print(timeid)
        print(thePeople)
        print(bid)
        
        mycursor.execute(query, (str(theDate), str(timeid), str(thePeople), str(bid),))
        conn.commit()

    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
        print("done")
    finally:
        mycursor.close()
        print("done2")

@dateTimeTable.route('/editPage/summaryEditPage/<bid>')
def summaryEditPage(bid):
    info = db_get_customerInfo(bid)
    info_list = info[0][0].split("/")
    theName = info_list[0]
    thePhone = info_list[1]
    theEmail = info_list[2]
    restBookInfo = db_get_restBookInfo(bid)
    theRestaurant = restBookInfo[0][0]
    theDate = restBookInfo[0][2]
    theTimeId= restBookInfo[0][3]
    thePeople = restBookInfo[0][4]
    theTime = db_get_time(theTimeId)
    theRestaurantName = get_restaurantName(theRestaurant)
    theBid = bid
    print("rid2 ", theRestaurant)
    return render_template("editPage/summaryEditPage.html", theDate=theDate, theTime=theTime,
                           theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, 
                           thePhone=thePhone, theEmail=theEmail, theBid=theBid, theRestaurantName=theRestaurantName)

@dateTimeTable.route('/editPage/updateBooking/<bid>', methods=["POST"])
def updateBooking(bid):
    theDate = request.form["theDate"]
    thePeople = request.form["thePeople"]
    theTime=request.form["theTime"]
    theName = request.form["theName"]
    thePhone = request.form["thePhone"]
    theEmail = request.form["theEmail"]
    theRestaurant=request.form["theRestaurant"]
    print("restaurant: ",theRestaurant)
    theBid = bid

    return render_template("editPage/update_rest_book.html", thePeople=thePeople,theDate=theDate,
                           theTime=theTime,theName=theName,thePhone=thePhone, theEmail=theEmail,
                           theRestaurant=theRestaurant, theBid=theBid)

@dateTimeTable.route('/editPage/UpdatenumberPeople', methods=["POST"])
def UpdatenumberPeople():
    
    theRestaurant = Restaurant.fetchRestaurant(request.form["theRestaurant"])
    return render_template("editPage/dateTimeEdit.html",restaurant=theRestaurant,
                           restaurantID=request.form["theRestaurant"])

@dateTimeTable.route('/editPage/UpdateDateEdit', methods=["POST"])
def UpdateDateEdit():

    people = request.form["people"]
    now = datetime.now()
    resto=request.form["theRestaurant"]
    restaurant=Restaurant.fetchRestaurant(request.form["theRestaurant"])
    weeks=calculCalendarWeeks(now)
    numbers=dayNumberCalendar(now)
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT * FROM period";
    mycursor.execute(query)
    periods=mycursor.fetchall()
    periodsOptions=buildSelectOptions(periods)
    calendarOptions=buildSelectOptions(weeks)
    db_insert_full_day()
    beginCalendar = now - timedelta(days=now.weekday())
    fullDays=daysDisabled(beginCalendar,periods[0][0])
    attendances=attendance(beginCalendar,periods[0][0])
    db_delete_full_day()
    templateCalendar=render_template('editPage/calendarEdit.html',numberCalendar=numbers, restaurant=restaurant,fullDays=fullDays,attendances=attendances)
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%Y-%m-%d"),"restaurantCapacity":50}
    return jsonify(response)

@dateTimeTable.route('/editPage/UpdatetimeEdit', methods=["POST"])
def UpdatetimeEdit():

    mycursor=app.config["DATABASE"].cursor()
    query="SELECT period FROM time_period WHERE time_period.time ='"+str(request.form["theTime"])+"';"
    mycursor.execute(query)
    period=mycursor.fetchall()[0][0]
    restaurant=Restaurant.fetchRestaurant(request.form["theRestaurant"])
    dateSelected=request.form["dateSelected"]
    # from db_methods
    times = db_get_times(period)
    query="SELECT timeid,TIME_FORMAT(time,'%H:%i') FROM time_period WHERE period='"+str(period)+"';"
    mycursor.execute(query)
    times=mycursor.fetchall()
    mycursor.execute("INSERT INTO booking_info VALUES(36,1,'01'),(37,2,'02'),(38,3,'03'),(39,3,'04'),(40,4,'05')")
    app.config["DATABASE"].commit()
    mycursor.execute("INSERT INTO rest_book VALUES(1,36,'01','2018-12-09',5,3),(1,37,'02','2018-12-09',5,2),(1,38,'03','2018-12-09',5,2),(1,39,'04','2018-12-09',5,2),(1,40,'05','2018-12-09',5,3)")
    app.config["DATABASE"].commit()
    fullTimes=timeDisabled(dateSelected,times,period)
    mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(36,37,38,39,40)")
    mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(36,37,38,39,40)")
    app.config["DATABASE"].commit()
    timesButton=buildTimesButtons(times,fullTimes=fullTimes)
    return render_template("editPage/timeEdit.html", times=timesButton,restaurant=restaurant)

@dateTimeTable.route('/editPage/removeBooking/<bid>', methods=["POST"])
def removeBooking(bid):
    
    remove_rest_book(bid)
    print(bid)
    return render_template("editPage/deletePage.html")

def remove_rest_book(bid):
    conn = app.config["DATABASE"]
    mycursor=conn.cursor()

    try:
        pass
        query = "DELETE FROM rest_book WHERE bid = %s"
        mycursor.execute(query, (str(bid),))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
        print("done")
    finally:
        mycursor.close()
        print("done2")


@dateTimeTable.route('/dateAndTime/changeCalendar', methods=["POST"])
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

def daysDisabled(beginCalendar,period):
    listTable=["01","02","03","04","05"]
    daysDisabled=[]
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

def attendance(beginCalendar,period):
    attendance=[]
    for i in range(0,14):
        attendance+=[db_get_attendance((beginCalendar+timedelta(days=i)).strftime("%Y-%m-%d"),period)]
    return attendance


