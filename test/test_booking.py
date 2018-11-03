
import pytest
import mysql.connector
import datetime
from src import app
from src import read_db_config
from src.views.dateTimeTable import calculCalendarWeeks

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