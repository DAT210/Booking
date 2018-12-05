from flask import Blueprint, render_template,request,jsonify
editPage = Blueprint('editPage', __name__,url_prefix="/editpage")
from src import app
from src.models import Restaurant
from datetime import datetime, timedelta
import mysql.connector
from src.views.dateTimeTable import calculCalendarWeeks,dayNumberCalendar,daysDisabled,timeDisabled
from src.templatebuild import buildSelectOptions,buildTimesButtons
from src.db_methods import db_get_time,db_get_restBookInfo,get_restaurantName,db_get_customerInfo,db_get_timeid,db_get_times,db_get_attendance,db_insert_full_day,db_delete_full_day

@editPage.route('/bookingsummary/<bid>',methods=["POST"])
def bookingSummary(bid):
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
    return render_template("editPage/bookingSummary.html", theDate=theDate, theTime=theTime,
                           theRestaurant=theRestaurant, theName=theName, thePeople=thePeople,
                           thePhone=thePhone, theEmail=theEmail, theBid=theBid,theRestaurantName=theRestaurantName)
@editPage.route('/removebooking/<bid>',methods=["POST"])
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

@editPage.route('/updatebooking/<bid>',methods=["POST"])
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


@editPage.route('/updatenumberpeople', methods=["POST"])
def UpdatenumberPeople():
    theRestaurant = Restaurant.fetchRestaurant(request.form["theRestaurant"])
    return render_template("editPage/dateTimeEdit.html",restaurant=theRestaurant.name,
                           restaurantID=request.form["theRestaurant"])

@editPage.route('/updatedateedit', methods=["POST"])
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

@editPage.route('/updatetimeedit', methods=["POST"])
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
    mycursor.execute("INSERT INTO rest_book VALUES(1,36,'01','2018-11-25',5,3),(1,37,'02','2018-11-25',5,2),(1,38,'03','2018-11-25',5,2),(1,39,'04','2018-11-25',5,2),(1,40,'05','2018-11-25',5,3)")
    app.config["DATABASE"].commit()
    fullTimes=timeDisabled(dateSelected,times,period)
    mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(36,37,38,39,40)")
    mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(36,37,38,39,40)")
    app.config["DATABASE"].commit()
    timesButton=buildTimesButtons(times,fullTimes=fullTimes)
    return render_template("editPage/timeEdit.html", times=timesButton,restaurant=restaurant)

@editPage.route('/tablevisualisationedit/<bid>', methods=["POST"])
def chooseTableSelectionEdit(bid):
    global selectedTime
    selectedTime=request.form["selectedTime"]
    theName=request.form["theName"]
    thePhone=request.form["thePhone"]
    theEmail=request.form["theEmail"]
    theRestaurant=Restaurant.fetchRestaurant(request.form["theRestaurant"])
    return render_template("editPage/buttonsTableEdit.html",restaurant=theRestaurant,theName=theName,thePhone=thePhone,theEmail=theEmail,theBid=bid)

@editPage.route('/checkbookingedit/<bid>', methods=["POST"])
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

def attendance(beginCalendar,period):
    attendance=[]
    for i in range(0,14):
        attendance+=[db_get_attendance((beginCalendar+timedelta(days=i)).strftime("%Y-%m-%d"),period)]
    return attendance