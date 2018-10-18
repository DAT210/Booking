
import pytest
import mysql.connector
from src import app
from python_mysql_dbconfig import read_db_config

@pytest.fixture
def client():
    app.config['DATABASE'] =read_db_config("static/config.ini")
    app.config['TESTING'] = True
    client = app.test_client()

def test_fetchAllRestaurant(client):

    mycursor = app.config['DATABASE'].cursor()
    mycursor.execute("SELECT * FROM restaurant")
    myresult = mycursor.fetchall()
    assert len(myresult)==1