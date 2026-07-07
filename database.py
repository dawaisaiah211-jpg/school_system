import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="shule_admin",
        password="Shule@2026",
        database="school_db"
    )
    return conn
