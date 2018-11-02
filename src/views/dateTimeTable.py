from flask import Blueprint, render_template, request
import datetime
from src import app
from models import Restaurant
from templatebuild import buildSelectOptions
from templatebuild import buildTimesButtons
now = datetime.datetime.now()

dateTimeTable = Blueprint('dateTimeTable', __name__)


@dateTimeTable.route("/dateAndTime", methods=["POST"])
def dateAndTime():
    global selectedRestaurant
    dateNow = now.strftime("%Y-%m-%d")
    restaurantID = int(request.form["restaurantID"])
    
    selectedRestaurant=Restaurant.fetchRestaurant(restaurantID)
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT * FROM period";
    mycursor.execute(query)
    periods=mycursor.fetchall()
    periodsOptions=buildSelectOptions(periods)
    return render_template('dateTimeTable/chooseDate.html', restaurant=selectedRestaurant,periods=periodsOptions)


@dateTimeTable.route('/dateAndTime/time', methods=["POST"])
def times():
    period=request.form["period"]
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT TIME_FORMAT(time,'%H:%i') FROM time_period WHERE period='"+str(period)+"';"
    mycursor.execute(query)
    times=mycursor.fetchall()
    timesButton=buildTimesButtons(times)
    return render_template("dateTimeTable/time.html", times=timesButton)


@dateTimeTable.route('/dateAndTime/checkBooking', methods=["POST"])
def dateAndTimeCheck():
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]
    theRestaurant = selectedRestaurant.name

    return render_template("dateTimeTable/confirmDate.html", theDate="2018-31-10", theTime="20:00", thePeople="2", 
    theRestaurant=theRestaurant, theName=theName, thePhone=thePhone, theEmail=theEmail)


