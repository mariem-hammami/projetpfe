import mysql.connector
import os
from dotenv import load_dotenv

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port = int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME") 
    )

def execute_fetchone(query, params = ()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result