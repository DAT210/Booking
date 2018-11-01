from flask import Blueprint, render_template, request
import datetime
from src import app
from models import Restaurant
from templatebuild import buildSelectOptions
from templatebuild import buildTimesButtons
from flask import jsonify

now = datetime.datetime.now()

dateTimeTable = Blueprint('dateTimeTable', __name__)


@dateTimeTable.route("/dateAndTime", methods=["POST"])
def dateAndTime():
    global restaurantID
    restaurantID = request.form["theRestaurant"]
    selectedRestaurant=Restaurant.fetchRestaurant(restaurantID)
    return render_template('dateTimeTable/dateTime.html', restaurant=selectedRestaurant)

@dateTimeTable.route("/dateAndTime/date", methods=["POST"])
def dateAndTimePeople():
    global people
    people = request.form["people"]
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT * FROM period";
    mycursor.execute(query)
    periods=mycursor.fetchall()
    periodsOptions=buildSelectOptions(periods)
    templateCalendar=render_template('dateTimeTable/calendar.html')
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people}
    return jsonify(response)



@dateTimeTable.route('/dateAndTime/time', methods=["POST"])
def times():
    period=request.form["period"]
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT TIME_FORMAT(time,'%H:%i') FROM time_period WHERE period='"+str(period)+"';"
    mycursor.execute(query)
    times=mycursor.fetchall()
    timesButton=buildTimesButtons(times)
    return render_template("dateTimeTable/time.html", times=timesButton)


@dateTimeTable.route('/dateAndTimeConfirmed', methods=["POST"])
def dateAndTimeConfirmed():
    theDate   = request.form["theDate"]
    theTime   = request.form["theTime"]
    theName   = request.form["theName"]
    thePeople = request.form["thePeople"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]


    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime,
    theRestaurant=restaurantID, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)

