from flask import Blueprint, render_template, request
from flask_mail import Mail, Message
from datetime import datetime
from src.db_methods import db_insert_booking, db_get_new_cid, db_get_timeid, db_get_bid
confirmPage = Blueprint('confirmPage', __name__)
from src import app
from src.models import Restaurant
mail = Mail(app)


@confirmPage.route('/confirmPage/step_6', methods=["POST"])
def bookedTables():
    json = request.get_json()
    bookedTables = ""

    for i, t in enumerate(json["tables"]):
        bookedTables += str(t)
        if i == len(json["tables"]) - 1:
            break
        bookedTables += ","
    return render_template("tableVisualization/checkBooking.html", bookedTables=bookedTables)


@confirmPage.route('/confirmPage/step_7', methods=["POST"])
def dateAndTimeCheck():
    theName = request.form["theName"]
    thePhone = request.form["thePhone"]
    theEmail = request.form["theEmail"]
    theRestaurant = Restaurant.fetchRestaurant(request.form["restaurant"])
    theRid = theRestaurant.rid
    theAddress = theRestaurant.street + ' , ' + str(theRestaurant.zip)
    theDate = datetime.date(datetime.strptime(request.form["date"], "%Y-%m-%d"))
    thePeople = request.form["people"]
    theTime = request.form["time"]
    theTables = request.form["tables"]

    if (theEmail != ''):  # if we confirm booking
        store_booking(theName, theEmail, theAddress, theDate, thePeople, theTime, theRid, theTables)
        # bid = db_get_bid(theEmail,theDate,theRid)
        send_mail(theName, theEmail, theRestaurant.name, theAddress, theDate.strftime("%d/%m/%Y"), thePeople, theTime,
                  "1")

    return render_template("confirmPage/confirmDate.html", theDate=theDate, theTime=theTime,
                           theRestaurant=theRestaurant.name, theName=theName, thePeople=thePeople, thePhone=thePhone,
                           theEmail=theEmail, rid=theRid, theTables=theTables)


def send_mail(name, email, restaurant, address, date, people, time, bid):
    subject = 'Confirmation of booking - 45610'
    message = 'Hello ' + name + ', <br> <br>You have booked a table for ' + people + ' people at : <br>' + restaurant + '<br>' + address + '<br>' + date + ' - ' + time + ' <br> To edit your reservation, click on the link below <br> http://localhost:5000/editBooking/' + bid + '<br> Best regards, <br> <br>' + restaurant
    msg = Message(
        subject=subject,
        recipients=[email],
        html=message
    )
    mail.send(msg)


def store_booking(theName, theEmail, theAddress, theDate, thePeople, theTime, theRid, theTables):
    date = theDate.strftime('%Y-%m-%d')
    cid = db_get_new_cid()  # this should be from the customer guys (theName, theEmail, theAddress) ->
    timeid = db_get_timeid(theTime)

    db_insert_booking(theRid, theTables, date, timeid, cid, thePeople,
                      "null")