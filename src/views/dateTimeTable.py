from flask import Blueprint, render_template, request
import datetime
from src import app
from models import Restaurant
from templatebuild import buildSelectOptions
now = datetime.datetime.now()

dateTimeTable = Blueprint('dateTimeTable', __name__)


@dateTimeTable.route("/dateAndTime", methods=["POST"])
def dateAndTime():
    global theRestaurant
    dateNow = now.strftime("%Y-%m-%d")
    print(dateNow)
    theRestaurant = request.form["theRestaurant"]
    print(theRestaurant)
    selectedRestaurant=Restaurant.fetchRestaurant(1)
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT * FROM period";
    mycursor.execute(query)
    periods=mycursor.fetchall()
    periodsOptions=buildSelectOptions(periods)
    return render_template('dateTimeTable/chooseDate.html', restaurant=selectedRestaurant,periods=periodsOptions)
    

@dateTimeTable.route('/dateAndTimeConfirmed', methods=["POST"])
def dateAndTimeConfirmed():
    theDate   = request.form["theDate"]
    theTime   = request.form["theTime"]
    theName   = request.form["theName"]
    thePeople = request.form["thePeople"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]


    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime, 
    theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)
