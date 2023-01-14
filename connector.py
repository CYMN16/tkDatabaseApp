# source: https://github.com/rimexe0/gameshop/blob/main/components/connector.py

import pymysql

# database credentials
hostName = "localhost"
userName = "root"
userPassword = "0000"
databaseName = "cymnflix"
databaseCharset = "utf8mb4"
cursorType = pymysql.cursors.DictCursor


def connect():
    try:
        databaseConnection = pymysql.connect(host=hostName,

                                             user=userName,

                                             password=userPassword,

                                             db=databaseName,

                                             charset=databaseCharset,

                                             cursorclass=cursorType)

        return databaseConnection
    except Exception as e:
        print("connection failed : {}".format(e))

# below functions are not used in this project
def callStoredProcedure(query, args):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.callproc(query, args)
        data = cur.fetchall()
        if len(data) == 0:
            conn.commit()
        else:
            print('error: ', str(data[0]))
    except Exception as e:
        print("query failed : {}".format(e))
    finally:
        conn.close()


def returnStoredProcedure(query, args):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.callproc(query, args)
        data = cur.fetchall()
        return data
    except Exception as e:
        print("returning stored procedure failed : {}".format(e))
    finally:
        conn.close()
