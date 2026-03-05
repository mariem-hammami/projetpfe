import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transport_db"  
    )

def verify_login(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT role FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    conn.close()
    return result