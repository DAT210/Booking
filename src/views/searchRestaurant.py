from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
import mysql.connector
#import requests
searchRestaurant = Blueprint('searchRestaurant', __name__)
from src import app
from src.models import Restaurant

conn = app.config["DATABASE"]

# sends along a tuple for each restaurant consisting of name,latitude,longitude
@searchRestaurant.route('/')
def index():
    names = []
    coords = []
    ids = []
    for r in restaurants:
        names.append((r.name))
        coords.append([r.latitude, r.longitude])
        ids.append((r.rid))
    return render_template('searchRestaurant/index.html', names=names, coords=coords,ids=ids)


def fetch_restaurants():
	cur = conn.cursor()
	try:
		sql = "SELECT * FROM restaurant"
		cur.execute(sql)
		restaurants = cur.fetchall()
	except mysql.connector.Error as err:
		print("Error: {}".format(err.msg))
	finally:
		cur.close()

	list_of_restaurants = []
	for r in restaurants:
		r1 = Restaurant(r[0], r[1], r[2], r[3], r[4], float(r[5]), float(r[6]))
		list_of_restaurants.append(r1)
	return list_of_restaurants


# global restaurant list
restaurants = fetch_restaurants()