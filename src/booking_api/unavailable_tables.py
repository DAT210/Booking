from flask import request, Blueprint
from flask_restful import Resource
from datetime import datetime, timedelta
from .db_methods import db_get_unavailable_tables, check_rid

periods = {
    1: "12:00",
    2: "14:00",
    3: "16:00",
    4: "18:00",
    5: "20:00",
    6: "22:00"
}

#checks if date and period are valid but not restaurant

class UnavailableTables(Resource):
    def get(self):

        if request.args["date"] and request.args["period"] and request.args["rid"]:
            date = request.args["date"]
            period = request.args["period"]
            rid = request.args["rid"]

            if checkDate(date) == 0:
                return {"Error": "Wrong syntax for date"}, 400
            elif checkDate(date) == 1:
                return {"Error": "We don't have data for this date"}, 400
            elif int(period) not in periods.keys():
                return {"Error": "No such period"}, 400
            elif not check_rid(rid):
                return {"Error": "No such restaurant"}, 400

            tables = db_get_unavailable_tables(date, period, rid)
        else:
            return {"Error": "Bad syntax"}, 400

        return {"Unvailable tables": tables, "date": date, "period": period}

# returns 0 if date string is of wrong format. Returns 1 if the request date is 2 months ahead of datetime.now()
def checkDate(datestr):
    try:
        req_date = datetime.strptime(datestr, "%Y-%m-%d")
    except ValueError:
        return 0

    if req_date > datetime.now() + timedelta(days=60) or req_date < datetime.now() :
        return 1

    return 2