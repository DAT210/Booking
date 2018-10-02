from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/thisIsHowToMakeRoute")
def thisRouteFunction():
    return "This is a route I just created"


if __name__ == '__main__':
    app.run()