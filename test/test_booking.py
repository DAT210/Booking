
import pytest
import mysql.connector
import datetime
from src import app
from src import read_db_config
from src.views.dateTimeTable import calculCalendarWeeks, dayNumberCalendar,isDayDisabled,isTimeDisabled
from src.db_methods import db_get_attendance

@pytest.fixture
def client():
    app.config['DATABASE'] = mysql.connector.connect(**read_db_config("config.ini"))
    app.config['TESTING'] = True
    client = app.test_client()

def test_fetchAllRestaurant(client):

    mycursor = app.config['DATABASE'].cursor()
    mycursor.execute("SELECT * FROM restaurant")
    myresult = mycursor.fetchall()
    assert len(myresult)==3

def test_calendarWeeks(client):
    errors = []
    now=datetime.datetime.now()
    weeks=calculCalendarWeeks(now)
    # replace assertions by conditions
    if not len(weeks)==3:
        errors.append("Not enough weeks")
    if not weeks[0][1]=="29/10 - 11/11":
        errors.append("first week is wrong")
    if not weeks[2][1]=="26/11 - 09/12":
        errors.append("last week is wrong")

    # assert no error message has been registered, else print messages
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_calanderDaysNumber(client):
    now=datetime.datetime.now()
    numbers=dayNumberCalendar(now)
    assert len(numbers)==14

def test_isDayDisabled(client):
    mycursor = app.config['DATABASE'].cursor()
    mycursor.execute("INSERT INTO booking_info VALUES(30,1,'01'),(31,2,'02'),(32,3,'03'),(33,3,'04'),(34,4,'05'),(35,5,'05')")
    app.config["DATABASE"].commit()
    mycursor.execute("INSERT INTO rest_book VALUES(1,30,'01','2018-11-13',5,2),(1,31,'02','2018-11-13',5,3),(1,32,'03','2018-11-13',5,4),(1,33,'04','2018-11-13',5,6),(1,34,'05','2018-11-13',5,4)")
    app.config["DATABASE"].commit()
    disabled=isDayDisabled(["01","02","03","04","05"],"2018-11-13","lunch")
    mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    assert disabled

def test_isTimeDisabled(client):
    mycursor = app.config['DATABASE'].cursor()
    mycursor.execute("INSERT INTO booking_info VALUES(30,1,'01'),(31,2,'02'),(32,3,'03'),(33,3,'04'),(34,4,'05'),(35,5,'05')")
    app.config["DATABASE"].commit()
    mycursor.execute("INSERT INTO rest_book VALUES(1,30,'01','2018-11-18',5,3),(1,31,'02','2018-11-18',5,2),(1,32,'03','2018-11-18',5,1),(1,33,'04','2018-11-18',5,2),(1,34,'05','2018-11-18',5,4)")
    app.config["DATABASE"].commit()
    disabled=isTimeDisabled("2018-11-18",[9],"lunch")
    mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    assert disabled

def test_attendance(client):
    mycursor = app.config['DATABASE'].cursor()
    mycursor.execute("INSERT INTO booking_info VALUES(30,1,'01'),(31,2,'02'),(32,3,'03'),(33,3,'04'),(34,4,'05'),(35,5,'05')")
    app.config["DATABASE"].commit()
    mycursor.execute("INSERT INTO rest_book VALUES(1,30,'01','2018-11-18',5,3),(1,31,'02','2018-11-18',5,2),(1,32,'03','2018-11-18',5,1),(1,33,'04','2018-11-18',5,2),(1,34,'05','2018-11-18',5,4)")
    app.config["DATABASE"].commit()
    attendance=db_get_attendance("2018-11-18","lunch")
    mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(30,31,32,33,34,35)")
    app.config["DATABASE"].commit()
    assert attendance==12