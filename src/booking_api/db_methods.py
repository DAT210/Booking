import mysql.connector
from src import app
mydb=app.config["DATABASE"]

def db_get_unavailable_tables(date, period_id, rid):
    cur = mydb.cursor()
    try:
        sql = "SELECT tid FROM rest_book WHERE date = %s AND peid = %s AND rid = %s"
        cur.execute(sql, (date, period_id, rid))
        tables = []
        for t in cur.fetchall():
            tables.append(t)
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        cur.close()
    return tables



def check_rid(rid):
    cur = mydb.cursor()
    check = True
    try:
        sql = "SELECT * FROM restaurant WHERE rid = %s"
        cur.execute(sql, (rid,))
        if len(cur.fetchall()) < 1:
            check = False
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        cur.close()
    return check