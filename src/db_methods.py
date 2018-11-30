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


def db_insert_booking(rid, tables, date, timeid, cid,people, add_info):
    mycursor = app.config["DATABASE"].cursor()
    try:
        sql = "INSERT INTO booking_info (cid,additional_info) VALUES (%s, %s)"
        mycursor.execute(sql, (str(cid), add_info))

        bid = db_get_bid(cid)

        for t in tables.split(","):
            sql = "INSERT INTO rest_book VALUES (%s, %s, %s, %s, %s,%s)"
            mycursor.execute(sql, (str(rid), str(bid), t, str(date), str(timeid),str(people)))

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
            "INSERT INTO booking_info VALUES(30,1,'01'),(31,2,'02'),(32,3,'03'),(33,3,'04'),(34,4,'05'),(50,5,'05'),(51,6,'05'),(52,7,'05'),(53,8,'05'),(54,5,'05'),(55,5,'05'),(56,5,'05'),(57,5,'05'),(58,5,'05'),(59,5,'05'),(60,5,'05'),(61,5,'05'),(62,5,'05')")
        app.config["DATABASE"].commit()
        mycursor.execute(
            "INSERT INTO rest_book VALUES(1,30,'01','2018-12-01',1,2),(1,31,'02','2018-12-01',1,2),(1,32,'03','2018-12-01',1,3),(1,33,'04','2018-12-01',1,3),(1,34,'05','2018-12-01',1,3),(1,50,'05','2018-12-02',1,6),(1,51,'05','2018-12-02',1,4),(1,52,'05','2018-12-02',1,4),(1,53,'05','2018-12-02',1,6),(1,54,'05','2018-12-02',1,3),(1,55,'05','2018-12-02',1,3),(1,56,'05','2018-12-02',1,3),(1,57,'05','2018-12-03',1,8),(1,58,'05','2018-12-03',1,8),(1,59,'05','2018-12-03',1,8),(1,60,'05','2018-12-03',1,8),(1,61,'05','2018-12-03',1,8),(1,62,'05','2018-12-03',1,3)")
        app.config["DATABASE"].commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()


def db_delete_full_day():  # Remove default fullDay
    mycursor = app.config['DATABASE'].cursor()
    try:
        mycursor.execute("DELETE FROM rest_book WHERE rest_book.bid IN(30,31,32,33,34,50,51,52,53,54,55,56,57,58,59,60,61,62)")
        mycursor.execute("DELETE FROM booking_info WHERE booking_info.bid IN(30,31,32,33,34,50,51,52,53,54,55,56,57,58,59,60,61,62)")
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

def db_get_attendance(date,period):
    mycursor = app.config['DATABASE'].cursor()
    try:
        sql = "SELECT SUM(people) FROM rest_book JOIN time_period on rest_book.timeid=time_period.timeid WHERE time_period.period=%s AND rest_book.date=%s"
        mycursor.execute(sql, (str(period),str(date)))
        sum=mycursor.fetchall()[0][0]
        if str(sum) !="None":
            return int(sum)
        return 0
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        mycursor.close()

# def db_check_tables(rid, date, timeid, tableids):
#     mycursor = app.config['DATABASE'].cursor()
#     print(rid)
#     print(date)
#     print(timeid)
#     try:
#         sql = "SELECT bid FROM rest_book WHERE rid=%s AND date=%s AND timeid=%s AND tid IN {0}".format(tuple(tableids))
#         print(sql)
#         mycursor.execute(sql, (str(rid), str(date), str(timeid)))
#         f = mycursor.fetchall()
#         print(f)
#         if len(f) != 0:
#             return 0
#         return 1
#     except mysql.connector.Error as err:
#         print("Error: {}".format(err.msg))
#     finally:
#         mycursor.close()