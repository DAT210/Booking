from flask import Blueprint, render_template, request

dateTimeTable = Blueprint('dateTimeTable', __name__)


@dateTimeTable.route("/dateAndTime")
def dateAndTime():
    return render_template('dateTimeTable/index.html')

@dateTimeTable.route('/dateAndTimeConfirmed', methods=["POST"])
def dateAndTimeConfirmed():
    theDate = request.form["theDate"]
    theTime = request.form["theTime"]

    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime)