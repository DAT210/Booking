import os
import sys
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from python_mysql_dbconfig import read_db_config
import mysql.connector
import time

currentPath=os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentPath)
currentPath=os.path.abspath(os.path.join(currentPath, os.pardir))
sys.path.append(currentPath)


app = Flask(__name__)
from views.searchRestaurant import searchRestaurant
from views.dateTimeTable import dateTimeTable
api = Api(app)
app.register_blueprint(searchRestaurant)
app.register_blueprint(dateTimeTable)

app.debug = True
docker =False
if docker:
    filename = "static/configDocker.ini"
else:
    filename = "static/config.ini"

db_config = read_db_config(filename)

mydb = mysql.connector.connect(**db_config)
app.config.from_mapping(DATABASE=mydb,)

periods = {
    "12:00": 1,
    "14:00": 2,
    "16:00": 3,
    "18:00": 4,
    "20:00": 5,
    "22:00": 6
}

# parser = reqparse.RequestParser()
# parser.add_argument("date", type=str)
# parser.add_argument("period", type=int)

class UnavailableTables(Resource):
    def get(self):
        # args = parser.parse_args()
        # date = args["date"]
        # period = args["period"]
        date = request.args["date"]
        period = request.args["period"]
        rid = request.args["rid"]

        try:
            time.strptime(date, "%Y-%m-%d")
        except ValueError:
            return {"Error": "Bad syntax"}, 400

        if period not in periods.keys():
            return {"Error": "Bad syntax"}, 400

        tables = db_get_unavailable_tables(date, period, rid)

        return {"Unvailable tables": tables, "date": date, "period": period}

api.add_resource(UnavailableTables, "/unavailabletables")


def db_get_unavailable_tables(date, period_id, rid):
    cur = mydb.cursor()
    try:
        sql = "SELECT tid FROM rest_book WHERE date = %s AND peid = %s AND rid = %s"
        cur.execute(sql, (date, period_id, rid))
        tables = []
        for t in cur.fetchall():
            tables.append(t)
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        cur.close()
    return tables



if __name__ == '__main__':

    if docker :
        app.run(host='0.0.0.0',port=5000)
    else :
        app.run()