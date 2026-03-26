from db.database import connect_db, execute_fetchall,execute_fetchone, execute_modifi
from flask import Flask, request, jsonify, Blueprint

gest_bus_bp = Blueprint("gest_bus", __name__)

@gest_bus_bp.route('/get_bus', methods = ['GET'])
def load_bus():
    try:
        query = "SELECT matricule_vehicule, type_vehicule, modele_vehicule FROM vehicule"
        rows = execute_fetchall(query)
        buses = []
        for r in rows:
            buses.append({"matricule":r[0],
                          "type":r[1],
                          "model":r[2]})
        return jsonify(buses)
    except Exception as e:
            return jsonify({"Erreur DB": str(e)})

@gest_bus_bp.route('/ajouter_bus', methods = ['POST'])
def ajouter_bus():
    data = request.json
    matricule = data.get('matricule')
    type_bus = data.get("type_bus")
    modele = data.get("modele")
    if matricule and type_bus and modele:
        query = "SELECT matricule_vehicule FROM vehicule WHERE matricule_vehicule = %s"
        is_exist = execute_fetchone(query, params = (matricule, ))
        if is_exist:
            return jsonify({"error":"bus already exists"})
        try:
            query = "INSERT INTO vehicule (matricule_vehicule, type_vehicule, modele_vehicule) VALUES (%s,%s,%s)"
            params = (matricule, type_bus, modele)
            execute_modifi(query, params)
            return jsonify({"Succès": "Bus ajouté !"})
        except Exception as e:
            return jsonify({"Erreur DB": str(e)})
    else:
        return jsonify({"error":"you must fill all fields to insert a new bus"})

@gest_bus_bp.route('/modifier_bus/<string:matricule>', methods = ['PUT'])
def modifier_bus(matricule):
    data = request.json
    new_type = data.get("new_type")
    new_modele = data.get("new_modele")
    if not new_type and not new_modele:
        return jsonify({"Champs manquants": "Veuillez remplir tous les champs"})
    query = "SELECT matricule_vehicule FROM vehicule WHERE matricule_vehicule = %s"
    params = (matricule,)
    is_exist = execute_fetchone(query, params)
    if not is_exist:
        return jsonify({"error": "bus not found"}),400
    if new_type and new_modele:
        try:
            query = "UPDATE vehicule SET type_vehicule=%s, modele_vehicule=%s WHERE matricule_vehicule=%s"
            params = (new_type, new_modele, matricule)
            execute_modifi(query, params = params)
            return jsonify ({"Succès": "Bus modifié !"})
        except Exception as e:
            return jsonify ({"Erreur DB": str(e)})
    if new_type and not new_modele:
        try: 
            query = "UPDATE vehicule SET type_vehicule=%s WHERE matricule_vehicule=%s"
            params = (new_type, matricule)
            execute_modifi(query, params = params)
            return jsonify ({"Succès": "Bus modifié !"})
        except Exception as e:
            return jsonify ({"Erreur DB": str(e)})
    if new_modele and not new_type:
        try:
            query = "UPDATE vehicule SET modele_vehicule=%s WHERE matricule_vehicule=%s"
            params = (new_modele, matricule)
            execute_modifi(query, params = params)
            return jsonify ({"Succès": "Bus modifié !"})
        except Exception as e:
            return jsonify ({"Erreur DB": str(e)})

@gest_bus_bp.route('/supprimer_bus/<string:matricule>', methods = ['DELETE'])
def supprimer_bus(matricule):
    query = "SELECT matricule_vehicule FROM vehicule WHERE matricule_vehicule = %s"
    params = (matricule,)
    is_exist = execute_fetchone(query, params=params)
    if not is_exist:
        return jsonify({"error": "bus not found"}),400
    try: 
        query = "DELETE FROM vehicule WHERE matricule_vehicule=%s" 
        params = (matricule,)
        execute_modifi(query, params = params)
        return jsonify ({"Succès": "Bus supprimé !"})
    except Exception as e:
        return jsonify({"Erreur DB", str(e)})