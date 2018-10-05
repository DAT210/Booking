
import pytest
import mysql.connector
from src import app

@pytest.fixture
def client():
    app.config['DATABASE'] = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="yourpassword",
        database="yourdatabase"
    )
    app.config['TESTING'] = True
    client = app.test_client()

def test_fetchAllRestaurant(client):

    mycursor = app.config['DATABASE'].cursor()
    mycursor.execute("SELECT * FROM restaurant")
    myresult = mycursor.fetchall()
    assert len(myresult)==1