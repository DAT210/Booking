from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from src import app
from src.models import Restaurant
from src.templatebuild import buildSelectOptions
from src.templatebuild import buildTimesButtons
from flask import jsonify


dateTimeTable = Blueprint('dateTimeTable', __name__)

#mail = Mail(app)


@dateTimeTable.route("/dateAndTime", methods=["POST"])
def dateAndTime():
    global selectedRestaurant
    global restaurantID
    restaurantID = request.form["theRestaurant"]
    selectedRestaurant=Restaurant.fetchRestaurant(restaurantID)
    return render_template('dateTimeTable/dateTime.html', restaurant=selectedRestaurant,restaurantID=restaurantID)

@dateTimeTable.route("/dateAndTime/date", methods=["POST"])
def dateAndTimePeople():
    global people
    people = request.form["people"]
    now = datetime.now()
    weeks=calculCalendarWeeks(now)
    numbers=dayNumberCalendar(now)
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT * FROM period";
    mycursor.execute(query)
    periods=mycursor.fetchall()
    periodsOptions=buildSelectOptions(periods)
    calendarOptions=buildSelectOptions(weeks)
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers)
    templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    response={"calendar" : templateCalendar,"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%d/%m/%Y")}
    return jsonify(response)



@dateTimeTable.route('/dateAndTime/time', methods=["POST"])
def times():
    period=request.form["period"]
    global dateSelected
    dateSelected=request.form["dateSelected"]
    mycursor=app.config["DATABASE"].cursor()
    query="SELECT TIME_FORMAT(time,'%H:%i') FROM time_period WHERE period='"+str(period)+"';"
    mycursor.execute(query)
    times=mycursor.fetchall()
    timesButton=buildTimesButtons(times)
    return render_template("dateTimeTable/time.html", times=timesButton)

@dateTimeTable.route('/dateAndTime/tableVisualisation', methods=["POST"])
def chooseTableSelection():
    global selectedTime
    selectedTime=request.form["selectedTime"]
    return render_template("dateTimeTable/buttonsTable.html",restaurant=Restaurant)

@dateTimeTable.route('/editPage/tableVisualisationEdit', methods=["POST"])
def chooseTableSelectionEdit():
    global selectedTime
    selectedTime=request.form["selectedTime"]
    theName=request.form["theName"]
    thePhone=request.form["thePhone"]
    theEmail=request.form["theEmail"]
    return render_template("editPage/buttonsTableEdit.html",restaurant=Restaurant,theName=theName,thePhone=thePhone,theEmail=theEmail)

@dateTimeTable.route('/dateAndTime/changeCalendar', methods=["POST"])
def changeCalendar():
    now=datetime.now()
    beginDate=request.form["beginDate"]
    numbers=dayNumberCalendar(datetime.strptime(beginDate, '%d-%m-%Y'))
    templateCalendar=render_template('dateTimeTable/calendar.html',numberCalendar=numbers)
    response={"calendar" : templateCalendar,"currentDay":now.strftime("%d/%m/%Y")}
    return jsonify(response)


@dateTimeTable.route('/dateAndTime/checkBooking', methods=["POST"])
def dateAndTimeCheck():
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]
    theRestaurant = selectedRestaurant.name
    theAddress = selectedRestaurant.street + ' , ' + str(selectedRestaurant.zip)
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime
    
    # if (theEmail != ''):
    #     send_mail(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime)

    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime,
    theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)

# def send_mail(name,email,restaurant,address,date,people,time):
#     subject = 'Confirmation of booking - 45610'
#     message = 'Hello '+name+', <br> <br>You have booked a table for '+people+' people at : <br>'+restaurant+'<br>'+address+'<br>'+date+' - '+time+' <br> To edit your reservation, click on the link below <br> http://localhost:5000 <br> Best regards, <br> <br>' + restaurant
#     msg = Message(
#         subject=subject,
#         recipients=[email], 
#         html=message
#     )
#     mail.send(msg)

@dateTimeTable.route('/editPage/checkBookingEdit', methods=["POST"])
def dateAndTimeCheckEdit():
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]
    theRestaurant = selectedRestaurant.name
    theAddress = selectedRestaurant.street + ' , ' + str(selectedRestaurant.zip)
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime
    
    # if (theEmail != ''):
    #     send_mail(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime)

    return render_template("editPage/confirmDateEdit.html", theDate=theDate, theTime=theTime,
    theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)

# def send_mail(name,email,restaurant,address,date,people,time):
#     subject = 'Confirmation of booking - 45610'
#     message = 'Hello '+name+', <br> <br>You have booked a table for '+people+' people at : <br>'+restaurant+'<br>'+address+'<br>'+date+' - '+time+' <br> To edit your reservation, click on the link below <br> http://localhost:5000 <br> Best regards, <br> <br>' + restaurant
#     msg = Message(
#         subject=subject,
#         recipients=[email], 
#         html=message
#     )
#     mail.send(msg)


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

@dateTimeTable.route('/editPage/summaryEditPage', methods=["POST"])
def summaryEditPage():
    theName = request.form["theName"]
    thePhone = request.form["thePhone"]
    theEmail = request.form["theEmail"]
    theRestaurant = selectedRestaurant.name
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime

    return render_template("editPage/summaryEditPage.html", theDate=theDate, theTime=theTime,
    theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail) 

# @dateTimeTable.route('/dateAndTime/removeBooking', methods=["POST"])
# def removeBooking():
#     return render_template("dateTimeTable/deletePage.html")

@dateTimeTable.route('/editPage/updateBooking', methods=["POST"])
def updateBooking():
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime
    theName = request.form["theName"]
    thePhone = request.form["thePhone"]
    theEmail = request.form["theEmail"]
    return render_template("/editPage/update_rest_book.html", thePeople=thePeople,theDate=theDate,
    theTime=theTime,theName=theName,thePhone=thePhone, theEmail=theEmail)

@dateTimeTable.route('/editPage/UpdatenumberPeople', methods=["POST"])
def UpdatenumberPeople():

    thePeople = people

    return render_template("editPage/dateTimeEdit.html", thePeople=thePeople,restaurant=selectedRestaurant,
    restaurantID=restaurantID)

@dateTimeTable.route('/editPage/UpdateDateEdit', methods=["POST"])
def UpdateDateEdit():

    people = request.form["people"]
    now = datetime.now()
    restaurant=selectedRestaurant
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


    # theDate = dateSelected
    # now = datetime.now()
    # restaurant=selectedRestaurant
    # numbers=dayNumberCalendar(now)
    # weeks=calculCalendarWeeks(now)
    # mycursor=app.config["DATABASE"].cursor()
    # query="SELECT * FROM period";
    # mycursor.execute(query)
    # periods=mycursor.fetchall()
    # periodsOptions=buildSelectOptions(periods)
    # calendarOptions=buildSelectOptions(weeks)
    # templateButtonsCalendar=render_template("dateTimeTable/rowCalendarButtons.html",periods=periodsOptions,weeks=calendarOptions)
    # response={"buttonsCalendar" : templateButtonsCalendar,"people" : people,"currentDay":now.strftime("%d/%m/%Y")}
    # return render_template("dateTimeTable/calendarEdit.html", theDate=theDate,numberCalendar=numbers, 
    #                         restaurant=restaurant, templateButtonsCalendar=templateButtonsCalendar,response=jsonify(response))


@dateTimeTable.route('/editPage/UpdatetimeEdit', methods=["POST"])
def UpdatetimeEdit():
   
    times=selectedTime

    return render_template("editPage/timeEdit.html", times=times)

@dateTimeTable.route('/editPage/removeBooking', methods=["POST"])
def removeBooking():
    cid=1
    rid = restaurantID
    print(cid)
    conn = app.config["DATABASE"]
    mycursor = conn.cursor()
    query = "SELECT bid FROM booking_info WHERE cid=%s "
    mycursor.execute(query,(str(cid),))
    bid = mycursor.fetchall()

    # conn = app.config["DATABASE"]
    # mycursor = conn.cursor()
    # query = "SELECT * FROM booking_info WHERE cid= %s"
    # # val = CONSEGUIR CID DE LA API?????
    # mycursor.execute(query, val)
    # booking_info = mycursor.fetchall()
    # bid = booking_info.1

    tid = 1

    remove_rest_book(rid,bid,tid)

    return render_template("editPage/deletePage.html")


def remove_rest_book(rid,bid,tid):
    conn = app.config["DATABASE"]
    mycursor=conn.cursor()

    # try:
    query = "DELETE FROM rest_book WHERE rid = %s AND bid = %s AND tid = %s" 
    mycursor.execute(query, (str(rid),str(bid),str(tid)))
    conn.commit()

    # except Error as error:
    #      print(error)
    
    # finally:
    # accept the change
    mycursor.close()

# @dateTimeTable.route('/dateAndTime/updateBooking', methods=["POST"])
# def updateBooking():
#     theName = request.form["theName"]
#     thePhone = request.form["thePhone"]
#     theEmail = request.form["theEmail"]
    
#     rid = restaurantID
    
#     conn = app.config["DATABASE"]
#     mycursor = conn.cursor()
#     query = "SELECT bid FROM booking_info WHERE cid= %"
#     # val = CONSEGUIR CID DE LA API?????
#     mycursor.execute(query, val)
#     bid = mycursor.fetchall()

#     # conn = app.config["DATABASE"]
#     # mycursor = conn.cursor()
#     # query = "SELECT * FROM booking_info WHERE cid= %"
#     # # val = CONSEGUIR CID DE LA API?????
#     # mycursor.execute(query, val)
#     # booking_info = mycursor.fetchall()
#     # bid = booking_info.1

#     # tid= COMO SE CONSIGUE

#     date=request.form["theDate"]

#     conn = app.config["DATABASE"]
#     mycursor = conn.cursor()
#     query = "SELECT timeid FROM time_period WHERE (time= %,period=%)"
#     # val = como conseguir period?
#     mycursor.execute(query, val)
#     timeid = mycursor.fetchall()

#     update_rest_book(rid, bid, tid, date, timeid)

#     return render_template('dateTimeTable/dateTime.html', restaurantID = restaurantID, restaurant=selectedRestaurant, 
#     theName=theName, thePhone=thePhone, theEmail=theEmail)

# def update_rest_book(rid, bid, tid, date, timeid):
#     conn = app.config["DATABASE"]
#     mycursor=conn.cursor()
#     # try:
#     query =  "UPDATE rest_book SET date = %s, time = %s WHERE (rid = %s, bid = %s, tid = %s)"
#     data = (date, peid, time, rid, bid, tid)
#     mycursor.execute(query, data)
#     conn.commit()

#     # except Error as error:
#     #      print(error)
    
#     # finally:
#     # accept the change
#     mycursor.close()