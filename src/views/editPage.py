from flask import Blueprint, render_template,request,jsonify
editPage = Blueprint('editPage', __name__,url_prefix="/editpage")
from src import app
from src.models import Restaurant
from datetime import datetime, timedelta
from src.views.dateTimeTable import calculCalendarWeeks,dayNumberCalendar,daysDisabled,timeDisabled
from src.templatebuild import buildSelectOptions,buildTimesButtons
from src.db_methods import db_get_times

@editPage.route('/bookingsummary',methods=["POST"])
def bookingSummary():
    print(request.form)
    theName = request.form["theName"]
    thePhone = request.form["thePhone"]
    theEmail = request.form["theEmail"]
    theRestaurant = Restaurant.fetchRestaurant(request.form["theRestaurant"])
    theDate = request.form["theDate"]
    thePeople = request.form["thePeople"]
    theTime=request.form["theTime"]

    return render_template("editPage/bookingSummary.html", theDate=theDate, theTime=theTime,
                           theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)
@editPage.route('/removeBooking',methods=["POST"])
def removeBooking():
    theName = request.form["theName"]
    thePhone = request.form["thePhone"]
    theEmail = request.form["theEmail"]
    theRestaurant = Restaurant.fetchRestaurant(request.form["theRestaurant"])
    theDate = request.form["theDate"]
    thePeople = request.form["thePeople"]
    theTime=request.form["theTime"]

    return render_template("editPage/bookingSummary.html", theDate=theDate, theTime=theTime,
                           theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)

@editPage.route('/updatebooking',methods=["POST"])
def updateBooking():
    theDate = request.form["theDate"]
    thePeople = request.form["thePeople"]
    theTime=request.form["theTime"]
    theName = request.form["theName"]
    thePhone = request.form["thePhone"]
    theEmail = request.form["theEmail"]
    theRestaurant=request.form["theRestaurant"]

    return render_template("editPage/update_rest_book.html", thePeople=thePeople,theDate=theDate,
                           theTime=theTime,theName=theName,thePhone=thePhone, theEmail=theEmail,theRestaurant=theRestaurant)


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
    templateCalendar=render_template('editPage/calendarEdit.html',numberCalendar=numbers, restaurant=restaurant)
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%d/%m/%Y")}
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

@editPage.route('/tablevisualisationedit', methods=["POST"])
def chooseTableSelectionEdit():
    global selectedTime
    selectedTime=request.form["selectedTime"]
    theName=request.form["theName"]
    thePhone=request.form["thePhone"]
    theEmail=request.form["theEmail"]
    theRestaurant=Restaurant.fetchRestaurant(request.form["theRestaurant"])
    return render_template("editPage/buttonsTableEdit.html",restaurant=theRestaurant,theName=theName,thePhone=thePhone,theEmail=theEmail)

@editPage.route('/checkbookingedit', methods=["POST"])
def dateAndTimeCheckEdit():
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]
    selectedRestaurant= Restaurant.fetchRestaurant(request.form["theRestaurant"])
    theAddress = selectedRestaurant.street + ' , ' + str(selectedRestaurant.zip)
    theDate = request.form["theDate"]
    thePeople = request.form["thePeople"]
    theTime=request.form["theTime"]

    # if (theEmail != ''):
    #     send_mail(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime)

    return render_template("editPage/confirmDateEdit.html", theDate=theDate, theTime=theTime,
                           theRestaurant=selectedRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)