from flask import Blueprint, render_template, request
from jinja2 import TemplateNotFound
from mysql.connector import MySQLConnection, Error
#from python_mysql_dbconfig import read_db_config
from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from src import app
from src.models import Restaurant
from src.templatebuild import buildSelectOptions
from src.templatebuild import buildTimesButtons
from flask import jsonify

editPage = Blueprint('editPage', __name__)

@editPage.route('/summaryEditPage', methods=["POST"])
def summaryEditPage():
    theName   = request.form["theName"]
    thePhone  = request.form["thePhone"]
    theEmail  = request.form["theEmail"]
    theRestaurant = selectedRestaurant.name
    theDate = dateSelected
    thePeople = people
    theTime=selectedTime

    return render_template("editPage/confirmDate.html", theDate=theDate, theTime=theTime,
    theRestaurant=theRestaurant, theName=theName, thePeople=thePeople, thePhone=thePhone, theEmail=theEmail)


# @editPage.route('/updateBooking', methods=["POST"])
# def update_rest_book(rid, bid, tid, date, peid, time):
#     # read database configuration
#     db_config = read_db_config()
 
#     # prepare query and data
#     query = """ UPDATE rest_book
#                 SET date = %s, time = %s
#                 WHERE bid = %s"""
 
#     data = (date, peid, time, rid, bid, tid)
 
#     try:
#         conn = MySQLConnection(**db_config)
 
#         # update res_book 
#         cursor = conn.cursor()
#         cursor.execute(query, data)
 
#         # accept the changes
#         conn.commit()
 
#     except Error as error:
#         print(error)
 
#     finally:
#         cursor.close()
#         conn.close()

# @editPage.route('/removeBooking', methods=["POST"])
# def delete_book(rid, bid, tid):
#     db_config = read_db_config()
 
#     query = "DELETE FROM rest_book WHERE rid = %s, bid = %s, tid = %s"
 
#     try:
#         # connect to the database server
#         conn = MySQLConnection(**db_config)
 
#         # execute the query
#         cursor = conn.cursor()
#         cursor.execute(query, (rid, bid, tid))
 
#         # accept the change
#         conn.commit()
 
#     except Error as error:
#         print(error)
 
#     finally:
#         cursor.close()
#         conn.close()

# @editPage.route('/comfirmEditDate', methods=["POST"])
# def editDateAndTimeConfirmed():
#     theEditDate   = request.form["theEditDate"]
#     theEditTime   = request.form["theEditTime"]
#     theEditPeople = request.form["theEditPeople"]
#     theDate   = request.form["theDate"]
#     theTime   = request.form["theTime"]
#     thePeople = request.form["thePeople"]

#     return render_template("editPage/confirmEditDate.html", theEditDate=theEditDate, theEditTime=theEditTime, 
#     theEditPeople=theEditPeople, theDate=theDate, theTime=theTime, thePeople=thePeople, theName=theName, 
#     theRestaurant = theRestaurant, thePhone=thePhone, theEmail=theEmail)