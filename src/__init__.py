from flask import Flask
from views.searchRestaurant import searchRestaurant
from views.dateTimeTable import dateAndTime
from views.dateTimeTable import dateAndTimeConfirmed

app = Flask(__name__)
app.register_blueprint(searchRestaurant)
app.register_blueprint(dateAndTime)
app.register_blueprint(dateAndTimeConfirmed)

app.debug = True

if __name__ == '__main__':
    app.run()