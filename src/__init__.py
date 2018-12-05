from flask import Flask
from flask_restful import Api
from flask_mail import Mail, Message
from flask_cors import CORS
import os
import sys
import mysql.connector
app = Flask(__name__)
app.config.from_mapping(APP_ROOT=os.path.dirname(os.path.abspath(__file__)))
app.config.from_mapping(APP_STATIC=os.path.join(app.config["APP_ROOT"], 'static'))
currentPath=os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentPath)
currentPath=os.path.abspath(os.path.join(currentPath, os.pardir))
sys.path.append(currentPath)
from src.python_mysql_dbconfig import read_db_config
docker = True
if docker:
    filename = "configDocker.ini"
else:
    filename = "config.ini"

db_config = read_db_config(filename)

mydb = mysql.connector.connect(**db_config)
app.config.from_mapping(DATABASE=mydb,)
CORS(app)
from src.views.searchRestaurant import searchRestaurant
from src.views.dateTimeTable import dateTimeTable
from src.views.confirmPage import confirmPage
from src.views.tableVisualization import tableVisualization
from src.views.editPage import  editPage
app.register_blueprint(searchRestaurant)
app.register_blueprint(dateTimeTable)
app.register_blueprint(confirmPage)
app.register_blueprint(tableVisualization)
app.register_blueprint(editPage)
#from src.booking_api.unavailable_tables import UnavailableTables

app.config.update(
    DEBUG=False,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=('no-reply', 'dat210.booking@gmail.com'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='dat210.booking@gmail.com',
    MAIL_PASSWORD='DAT210_booking'
)

mail = Mail(app)

app.debug = True
CORS(app)
if __name__ == '__main__':

    if docker :
        app.run(host='0.0.0.0',port=4001)
    else :
        app.run(port=4001)