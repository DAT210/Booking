import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="root",
	database="dat210_booking"
)

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