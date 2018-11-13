from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from datetime import datetime
from src import app
from src.models import Restaurant
from src.templatebuild import buildSelectOptions
from src.templatebuild import buildTimesButtons
from flask import jsonify


dateTimeTable = Blueprint('dateTimeTable', __name__)

mail = Mail(app)


@dateTimeTable.route("/dateAndTime", methods=["POST"])
def dateAndTime():
    global selectedRestaurant
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
    theRid = selectedRestaurant.rid
    theAddress = selectedRestaurant.street + ' , ' + str(selectedRestaurant.zip)
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime
    
    if (theEmail != ''): #if we confirm booking
        send_mail(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime)
        send_reservation_to_db(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime,theRid)

    return render_template("dateTimeTable/confirmDate.html", theDate=theDate, theTime=theTime,
    theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)

def send_mail(name,email,restaurant,address,date,people,time):
    subject = 'Confirmation of booking - 45610'
    message = 'Hello '+name+', <br> <br>You have booked a table for '+people+' people at : <br>'+restaurant+'<br>'+address+'<br>'+date+' - '+time+' <br> To edit your reservation, click on the link below <br> http://localhost:5000 <br> Best regards, <br> <br>' + restaurant
    msg = Message(
        subject=subject,
        recipients=[email], 
        html=message
    )
    mail.send(msg)  
    
def send_reservation_to_db(theName,theEmail,theRestaurant,theAddress,theDate,thePeople,theTime,theRid):
    mycursor=app.config['DATABASE'].cursor()
    #connect with the other group responsible for the user accounts
    #send them information about customer
    cid = get_new_cid() #get customer id from them in the future
    
    date = datetime.strptime(theDate, '%d/%M/%Y')
    date = datetime.date(date)
    timeid = get_timeid(theTime)

    query1="INSERT INTO booking_info (cid,additional_info) VALUES ("+str(cid)+",null);"
    mycursor.execute(query1)
    
    bid = get_bid(cid)
    query2="INSERT INTO rest_book VALUES ("+str(theRid)+","+str(bid)+",0,'"+str(date)+"','"+str(timeid)+"');" #define tid (tableID) as 0 for the moment
    mycursor.execute(query2)
    
    app.config['DATABASE'].commit()
    return 

def get_new_cid():
    mycursor=app.config['DATABASE'].cursor()
    query="SELECT cid FROM booking_info ORDER BY cid DESC LIMIT 1;"
    mycursor.execute(query)
    last_cid = mycursor.fetchall()
    mycursor.close()
    try :
            #if the table is not empty we return id + 1, otherwise 0
            return last_cid[0][0] + 1
    except:
        return 0
    
def get_timeid(time):
    mycursor=app.config['DATABASE'].cursor()
    query="SELECT timeid FROM time_period WHERE time='"+time+"';"
    mycursor.execute(query)
    timeid = mycursor.fetchall()
    mycursor.close()
    return timeid[0][0]
    

def get_bid(cid):
    mycursor=app.config['DATABASE'].cursor()
    query="SELECT bid FROM booking_info WHERE cid='"+str(cid)+"';"
    mycursor.execute(query)
    bid = mycursor.fetchall()
    mycursor.close()
    return bid[0][0]

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



