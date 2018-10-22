from src import app
class Restaurant :
    def __init__(self,rid, name, phone, zip, street):
        self.rid=rid
        self.name = name
        self.phone = phone
        self.zip = zip
        self.street = street

    def fetchRestaurant(id):
        mycursor=app.config['DATABASE'].cursor()
        query="SELECT * FROM restaurant WHERE rid="+str(id)+";"
        mycursor.execute(query)
        myresult=mycursor.fetchall()
        restaurant=Restaurant(myresult[0][0],myresult[0][1],myresult[0][2],myresult[0][3],myresult[0][4])
        return restaurant
