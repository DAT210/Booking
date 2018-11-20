from flask import Flask
from flask_restful import Api
from flask_mail import Mail, Message
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
from src.views.confirmPage import confirmPage
from src.views.tableVisualization import tableVisualization
app.register_blueprint(searchRestaurant)
app.register_blueprint(dateTimeTable)
app.register_blueprint(confirmPage)
app.register_blueprint(tableVisualization)
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
if __name__ == '__main__':

    if docker :
        app.run(host='0.0.0.0',port=5000)
    else :
        app.run()