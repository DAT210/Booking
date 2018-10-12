from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

searchRestaurant = Blueprint('searchRestaurant', __name__)
from src import app

@searchRestaurant.route('/')
def index():
    return render_template('searchRestaurant/index.html')