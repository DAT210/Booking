from flask import Blueprint, render_template, request

dateTimeTable = Blueprint('dateTimeTable', __name__)


@dateTimeTable.route("/dateAndTime")
def dateAndTime():
    return render_template('dateTimeTable/index.html', restaurant="NameOfRestaurant", 
    address="Address", telephone="Tel")
    

@dateTimeTable.route('/dateAndTimeConfirmed', methods=["POST"])
def dateAndTimeConfirmed():
    theDate = request.form["theDate"]
    theTime = request.form["theTime"]

    if(theDate == ""):
        print("Date not set!")
        return render_template('dateTimeTable/index.html', err="Date not set!")
    if(theTime == ""):
        print("Time not set!")
        return render_template('dateTimeTable/index.html', err="Time not set!")

    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime)