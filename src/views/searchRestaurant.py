from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
import mysql.connector
import requests
searchRestaurant = Blueprint('searchRestaurant', __name__)
from src import app
from src.models import Restaurant
from datetime import timedelta

# sends along a tuple for each restaurant consisting of name,latitude,longitude
@searchRestaurant.route('/')
def index():
	names = []
	coords = []
	ids = []
	opening_hours = []
	for r in restaurants:
		names.append(r.name)
		coords.append([r.latitude, r.longitude])
		ids.append(r.rid)
		opening_hours.append(db_fetch_opening_hours(r.rid))
	return render_template('searchRestaurant/index.html', names=names, coords=coords,ids=ids, opening_hours=opening_hours)


def db_fetch_restaurants():
	mycursor = app.config["DATABASE"].cursor()
	try:
		sql = "SELECT * FROM restaurant"
		mycursor.execute(sql)
		restaurants = mycursor.fetchall()
	except mysql.connector.Error as err:
		print("Error: {}".format(err.msg))
	finally:
		mycursor.close()

	list_of_restaurants = []
	for r in restaurants:
		r1 = Restaurant(r[0], r[1], r[2], r[3], r[4], float(r[5]), float(r[6]))
		list_of_restaurants.append(r1)
	return list_of_restaurants


# global restaurant list
restaurants = db_fetch_restaurants()

def db_fetch_opening_hours(rid):
	mycursor = app.config["DATABASE"].cursor()
	try:
		sql = "SELECT weekdays_open, weekdays_close, satsun_open, satsun_close FROM opening_hours WHERE rid=%s"
		mycursor.execute(sql, (str(rid),))
		tuple_of_data = mycursor.fetchall()[0]
	except mysql.connector.Error as err:
		print("Error: {}".format(err.msg))
        
	finally:
		mycursor.close()

	opening_hours = []
	for d in tuple_of_data:
		if len(str(d)) == 7:  # times with hours 00-09 becomes 0-9
			newstr = "0" + str(d)[0:4]
			opening_hours.append(newstr)
			continue
		opening_hours.append(str(d)[0:5])
	return opening_hours