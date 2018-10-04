from flask import Flask
from src.views.searchRestaurant import searchRestaurant
from src.views.dateTimeTable import dateTimeTable
import mysql.connector

app = Flask(__name__)
app.register_blueprint(searchRestaurant)
app.register_blueprint(dateTimeTable)

app.debug = True

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="yourpassword",
    database="yourdatabase"
)
app.config.from_mapping(DATABASE=mydb,)
if __name__ == '__main__':
    app.run()