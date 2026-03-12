import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="server680404.ddns.net",
        port=3368,
        user="user_srtb",
        password="SRTB!2026@",
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