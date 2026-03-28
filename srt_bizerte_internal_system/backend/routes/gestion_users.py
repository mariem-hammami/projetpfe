from flask import Flask, request, Blueprint, jsonify
from db.database import connect_db, execute_fetchall, execute_fetchone, execute_modifi
from werkzeug.security import generate_password_hash

gest_user_bp = Blueprint("/gest_user", __name__)

@gest_user_bp.route("/get_users", methods = ['GET'])
def get_users():
    try:
        query = "SELECT id, username, role FROM users"
        rows = execute_fetchall(query)
        if not rows:
            return jsonify({"error": "table users is empty"})
        users = []
        for r in rows:
            users.append({"id": r[0],
                "username":r[1],
                "role":r[2]})
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@gest_user_bp.route("/get_user/<int:id>", methods = ['GET'])
def get_user(id):
    query = "SELECT id, username, role FROM users WHERE id = %s"
    try:
        row = execute_fetchone(query, params = (id,))
        if not row:
            return jsonify({"error": "user not found"}),404
        return jsonify({"id":row[0], "username":row[1], "role":row[2]}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@gest_user_bp.route("/add_user", methods = ['POST'])
def add_user():
    data = request.json
    username = data.get("username")
    role = data.get("role")
    department = data.get("department")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error":"you must enter username or a temporary password"}),400
    try:
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO users (username, password, role) VALUES(%s, %s, %s)"
        params = (username,hashed_password,  role)
        add_user_id = execute_modifi(query, params = params)
        return jsonify({"message":"user created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@gest_user_bp.route("/update_user/<int:id>", methods = ['PUT'])
def update_user(id):
    data = request.json
    new_username = data.get("new_username")
    new_role = data.get("new_role")
    new_dep = data.get("new_dep")
    user = execute_fetchone("SELECT username, role FROM users WHERE id = %s", (id,))
    if not user:
        return jsonify({"error":"user not found"}), 404
    if not new_username:
        new_username = user[0]
    if not new_role:
        new_role = user[1]
    query = "SELECT id FROM users WHERE username = %s AND role = %s AND id = %s"
    params = (new_username, new_role, id)
    row = execute_fetchone(query, params = params)
    if row:
        return jsonify({"error":"modification is failed because another user has the same information or you don't update anything"})
    try:
        query = "UPDATE users SET username = %s, role = %s WHERE id = %s"
        execute_modifi(query, params = params)
        return jsonify({"success":"user updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@gest_user_bp.route("/delete_user/<int:id>", methods = ['DELETE'])
def delete_user(id):
    user = execute_fetchone("SELECT username, role FROM users WHERE id = %s", (id,))
    if not user:
        return jsonify({"error":"user not found"}), 404
    try:
        query = "DELETE FROM users WHERE id = %s"
        execute_modifi(query, params = (id,))
        return jsonify({"success":"user deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400