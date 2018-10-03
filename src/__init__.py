from flask import Flask
from views.searchRestaurant import searchRestaurant
from views.dateTimeTable import dateTimeTable

app = Flask(__name__)
app.register_blueprint(searchRestaurant)
app.register_blueprint(dateTimeTable)

app.debug = True

if __name__ == '__main__':
    app.run()