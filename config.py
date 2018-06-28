from .settings import HOST,NAME, USER, PASSWORD
import psycopg2

def db_connection():
    # Define our connection string
    conn_string = "host='"+HOST+"' dbname='"+NAME+"' user='"+USER+"' password='"+PASSWORD+"'"

    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    try:
        CONN = psycopg2.connect(conn_string)
    except:
        print ("Unable to connect to database")
    # conn.cursor will return a cursor object, you can use this cursor to perform queries

    return CONN