import pymysql

class MySql(object):

    USER     = None
    PASSWORD = None
    HOST     = None
    DATABASE = None

    def __init__(self, host, user, password, database):
        global USER, PASSWORD, HOST, DATABASE
        USER        = user
        PASSWORD    = password
        HOST        = host
        DATABASE    = database

    def connect(self):
        return pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, connect_timeout=5);
