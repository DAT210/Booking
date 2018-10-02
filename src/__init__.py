from flask import Flask
from views.searchRestaurant import searchRestaurant

app = Flask(__name__)
app.register_blueprint(searchRestaurant)

app.debug = True

if __name__ == '__main__':
    app.run()