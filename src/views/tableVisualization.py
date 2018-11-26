from flask import Blueprint, render_template,request
from src.db_methods import db_get_unavailable_tables
tableVisualization = Blueprint('tableVisualization', __name__)
from src.models import Restaurant

@tableVisualization.route('/step_4/tableVisualization', methods=["POST"])
def showButtons():
    global selectedTime
    selectedTime=request.form["selectedTime"]
    return render_template("tableVisualization/buttonsTable.html")

@tableVisualization.route('/step_5/tableVisualization', methods=["POST"])
def unavailableTables():
    unvTables = db_get_unavailable_tables(selectedRestaurant.rid,selectedTime, dateSelected)
    return jsonify(tables=unvTables, nrOfPeople=people)
