import os
import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host="mysql-325837d0-dawaisaiah211-4d7a.h.aivencloud.com",
        port=11209,
        user="avnadmin",
        password=os.environ.get("DB_PASSWORD"),
        database="defaultdb"
    )
    return conn
