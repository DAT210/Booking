from flask import Flask
from flask_restful import Api
import os
import sys
from python_mysql_dbconfig import read_db_config
import mysql.connector

currentPath=os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentPath)
currentPath=os.path.abspath(os.path.join(currentPath, os.pardir))
sys.path.append(currentPath)


app = Flask(__name__)
from views.searchRestaurant import searchRestaurant
from views.dateTimeTable import dateTimeTable

app.register_blueprint(searchRestaurant)
app.register_blueprint(dateTimeTable)

from booking_api.unavailable_tables import UnavailableTables
api = Api(app)
api.add_resource(UnavailableTables, "/tables")

app.debug = True
docker =False
if docker:
    filename = "static/configDocker.ini"
else:
    filename = "static/config.ini"

db_config = read_db_config(filename)

mydb = mysql.connector.connect(**db_config)
app.config.from_mapping(DATABASE=mydb,)


if __name__ == '__main__':

    if docker :
        app.run(host='0.0.0.0',port=5000)
    else :
        app.run()