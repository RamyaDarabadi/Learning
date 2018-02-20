import pymysql

def get_pymysql_connection():
    connect = pymysql.connect(host = "localhost" , user = "root", password = '', db = 'travelblogs', charset = "utf8mb4")
    cursor = connect.cursor()
    return connect,cursor
