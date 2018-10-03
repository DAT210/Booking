from flask import Blueprint, render_template

dateTimeTable = Blueprint('dateTimeTable', __name__)

@dateTimeTable.route("/thisIsHowToMakeRoute")
def thisRouteFunction():
    return "This is a route I just created"