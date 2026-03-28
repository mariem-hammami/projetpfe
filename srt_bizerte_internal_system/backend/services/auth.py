from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from db.database import execute_fetchone, execute_modifi

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get("user_id")
    username = data.get('username')
    role = data.get('role')
    password = data.get('password')
    if not (user_id and username and role and password):
            return jsonify({"error": "missing information"}),400
    try:
        query = "SELECT id, username, role, password FROM users WHERE id = %s AND username=%s AND role =%s"
        user = execute_fetchone(query, (user_id, username, role))
        if not user:
            return ({"error":"user not found please check the information you entered"}),404
        hash_password = user[3]
        if not check_password_hash(hash_password, password):
            return jsonify({"message": "Invalid credentials"}), 401

        return jsonify({"message": "Login successful", "user": user}),200
    except Exception as e:
        return jsonify({"error":str(e)})
   
        

@auth_bp.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    user_id = data.get("user_id")
    username = data.get("username")
    role = data.get("role")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    try:
        if not (user_id and username and role and old_password and new_password):
            return jsonify({"error": "missing information"}),400
        query = "SELECT password FROM users WHERE id = %s and username = %s and  role = %s"
        params = (user_id, username, role)
        password = execute_fetchone(query, params = params)
        if not password:
            return ({"error":"user not found please check the information you entered"}),404
        if not check_password_hash(password[0], old_password):
            return jsonify({"error":"please check your password"}), 401
        hash_password = generate_password_hash(new_password)
        query = "UPDATE users SET password = %s WHERE id = %s"
        params = (hash_password, user_id)
        execute_modifi(query, params = params)
        return jsonify({"success":"password updated successfully"}), 200
    except Exception as e:
        return jsonify({"error":str(e)})
    



