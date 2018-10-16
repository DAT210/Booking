from flask import Blueprint, render_template, request

dateTimeTable = Blueprint('dateTimeTable', __name__)


@dateTimeTable.route("/dateAndTime", methods=["POST"])
def dateAndTime():
    global theRestaurant
    theRestaurant = request.form["theRestaurant"]
    return render_template('dateTimeTable/chooseDate.html', restaurant=theRestaurant,
     telephone="555 55 555")
    

@dateTimeTable.route('/dateAndTimeConfirmed', methods=["POST"])
def dateAndTimeConfirmed():
    theDate   = request.form["theDate"]
    theTime   = request.form["theTime"]
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]


    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime, 
    theRestaurant=theRestaurant, thePeople=thePeople, theName=theName, thePhone=thePhone, theEmail=theEmail)