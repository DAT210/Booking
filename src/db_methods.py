from src import app
import mysql.connector

def db_get_periods():
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "SELECT * FROM period"
        mycursor.execute(sql)
        periods = mycursor.fetchall()
        return periods
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()

def db_get_times(period):
    mycursor=app.config["DATABASE"].cursor()
    try:
        sql = "SELECT timeid,TIME_FORMAT(time,'%H:%i') FROM time_period WHERE period=%s"
        mycursor.execute(sql, (str(period),))
        times = mycursor.fetchall()
        return times
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()

def db_get_unavailable_tables(rid, time, date):
    timeid = db_get_timeid(time)
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "SELECT tid FROM rest_book WHERE rid=%s AND timeid=%s AND date=%s"
        mycursor.execute(sql, (rid, timeid, date))
        unvTables = mycursor.fetchall()
        return unvTables
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()

def db_get_timeid(time):
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "SELECT timeid FROM time_period WHERE time=%s"
        mycursor.execute(sql, (time,))
        timeid = mycursor.fetchall()
        return timeid[0][0]
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()

def db_get_unavailable_tables(rid, time, date):
    timeid = db_get_timeid(time)
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "SELECT tid FROM rest_book WHERE rid=%s AND timeid=%s AND date=%s"
        mycursor.execute(sql, (rid, timeid, date))
        unvTables = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()
    return unvTables


def db_insert_booking(rid, tid, date, timeid, cid, add_info):
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "INSERT INTO booking_info (cid,additional_info) VALUES (%s, %s)"
        mycursor.execute(sql, (str(cid), add_info))

        bid = db_get_bid(cid)

        sql = "INSERT INTO rest_book VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(sql, (str(rid), str(bid), str(tid), str(date), str(timeid)))

        app.config["DATABASE"].commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()


def db_get_bid(cid):
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "SELECT bid FROM booking_info WHERE cid=%s;"
        mycursor.execute(sql, (str(cid),))
        bid = mycursor.fetchall()
        return bid[len(bid) - 1][0] # the last inserted booking for that customer
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()


def db_get_new_cid():
    mycursor = app.config['DATABASE'].cursor()

    try:
        sql = "SELECT cid FROM booking_info ORDER BY cid DESC LIMIT 1;"
        mycursor.execute(sql)
        last_cid = mycursor.fetchall()
        try:
            # if the table is not empty we return id + 1, otherwise 0
            return last_cid[0][0] + 1
        except:
            return 0
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()


def db_insert_full_day(): # Default fullDay
    mycursor = app.config['DATABASE'].cursor()
    try:
        mycursor.execute(
            "INSERT INTO booking_info VALUES(30,1,'01'),(31,2,'02'),(32,3,'03'),(33,3,'04'),(34,4,'05'),(35,5,'05')")
        mycursor.execute(
            "INSERT INTO rest_book VALUES(1,30,'01','2018-11-17',1),(1,31,'02','2018-11-17',1),(1,32,'03','2018-11-17',1),(1,33,'04','2018-11-17',1),(1,34,'05','2018-11-17',1)")
        app.config["DATABASE"].commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()


def db_delete_full_day():  # Remove default fullDay
    mycursor = app.config['DATABASE'].cursor()
    try:
        mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(30,31,32,33,34,35)")
        mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(30,31,32,33,34,35)")
        app.config["DATABASE"].commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()

def db_get_times_from_period(period):
    mycursor = app.config['DATABASE'].cursor()
    try:
        sql = "SELECT time_period.timeid FROM time_period WHERE period=%s"
        mycursor.execute(sql, (str(period),))
        return mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()