from flask import Blueprint, render_template,request, json
from jinja2 import TemplateNotFound
import mysql.connector
import requests
from datetime import datetime
from src.db_methods import db_get_unavailable_tables, db_get_timeid, db_check_tables
tableVisualization = Blueprint('tableVisualization', __name__)
from src import app
from src.models import Restaurant
from flask import jsonify

@tableVisualization.route('/tableVisualization/step_4', methods=["POST"])
def showButtons():
    return render_template("tableVisualization/buttonsTable.html", restaurant=Restaurant)

@tableVisualization.route('/tableVisualization/step_5', methods=["POST"])
def unavailableTables():
    date = request.form["date"]
    time = request.form["time"]
    rid = request.form["time"]
    people = request.form["people"]
    unvTables = db_get_unavailable_tables(rid, time, date)
    return jsonify(tables=unvTables, nrOfPeople=people)

# @tableVisualization.route('/tableVisualization/availability', methods=["POST"])
# def checkAvailability():
#     json = request.get_json()
#     date = datetime.date(datetime.strptime(json["date"], "%Y-%m-%d"))
#     rid = json["rid"]
#     timeid = db_get_timeid(json["time"])
#     # mysql_list = "("
#     # for i, t in enumerate(json["tables"]):
#     #     mysql_list += str(t)
#     #     if i != len(json["tables"]) - 1:
#     #         mysql_list += ","
#     #     else:
#     #         mysql_list += ")"
#
#     check = db_check_tables(rid, date, timeid, json["tables"])
#     return jsonify(check=str(check))