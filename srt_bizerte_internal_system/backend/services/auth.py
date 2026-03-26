from flask import Blueprint, request, jsonify
from db.database import execute_fetchone

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

   
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    user = execute_fetchone(query, (username, password))

    if user:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

