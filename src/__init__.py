from flask import Flask
from flask_restful import Api
import os
import sys
import mysql.connector
app = Flask(__name__)
app.config.from_mapping(APP_ROOT=os.path.dirname(os.path.abspath(__file__)))
app.config.from_mapping(APP_STATIC=os.path.join(app.config["APP_ROOT"], 'static'))
from src.python_mysql_dbconfig import read_db_config
docker =False
if docker:
    filename = "configDocker.ini"
else:
    filename = "config.ini"

db_config = read_db_config(filename)

mydb = mysql.connector.connect(**db_config)
app.config.from_mapping(DATABASE=mydb,)
from src.views.searchRestaurant import searchRestaurant
from src.views.dateTimeTable import dateTimeTable
app.register_blueprint(searchRestaurant)
app.register_blueprint(dateTimeTable)
from src.booking_api.unavailable_tables import UnavailableTables
api = Api(app)
api.add_resource(UnavailableTables, "/tables")

app.debug = True
if __name__ == '__main__':

    if docker :
        app.run(host='0.0.0.0',port=5000)
    else :
        app.run()