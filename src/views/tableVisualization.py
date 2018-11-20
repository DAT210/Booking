from flask import Blueprint, render_template,request
from jinja2 import TemplateNotFound
import mysql.connector
import requests
from src.db_methods import db_get_unavailable_tables
tableVisualization = Blueprint('tableVisualization', __name__)
from src import app
from src.models import Restaurant

@tableVisualization.route('/tableVisualization/step_4', methods=["POST"])
def showButtons():
    global selectedTime
    selectedTime=request.form["selectedTime"]
    return render_template("templates/tableVisualization/buttonsTable.html", restaurant=Restaurant)

@tableVisualization.route('/tableVisualization/step_5', methods=["POST"])
def unavailableTables():
    unvTables = db_get_unavailable_tables(selectedRestaurant.rid,selectedTime, dateSelected)
    return jsonify(tables=unvTables, nrOfPeople=people)
