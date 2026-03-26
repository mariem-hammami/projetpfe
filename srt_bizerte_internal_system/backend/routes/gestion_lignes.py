import tkinter as tk
from tkinter import ttk, messagebox
from db.database import connect_db, execute_fetchall, execute_modifi, execute_fetchone
from flask import Blueprint, request, jsonify

gest_ligne_bp = Blueprint('gest_ligne', __name__)

@gest_ligne_bp.route('/get_ligne', methods = ['GET'])
def load_lignes():
    query = "SELECT id_ligne, libelle_ligne, id_agence FROM ligne"
    lignes_rows = execute_fetchall(query)
    lignes = []
    for ligne in lignes_rows:
        lignes.append({"ligne_ID":ligne[0],
                      "Name": ligne[1],
                      "Agence_ID":ligne[2]})
    return jsonify(lignes)

@gest_ligne_bp.route('/ajouter_ligne', methods = ['POST'])
def ajouter_ligne():
    data = request.json
    libelle = data.get('libelle')
    id_agence = data.get('id_agence')
    query = "SELECT id_ligne from ligne WHERE libelle_ligne = %s AND id_agence=%s" 
    params = (libelle, id_agence)
    is_exist = execute_fetchone(query, params = params)
    if is_exist:
        return jsonify({"message":"ligne already exist!"})
    try:
        query = "INSERT INTO ligne (libelle_ligne, id_agence) VALUES (%s, %s)"
        execute_modifi(query, params)
        return jsonify({"Succès": "Ligne ajoutée avec ID"})
    except Exception as e:
        return jsonify({"Erreur DB": str(e)})
    
@gest_ligne_bp.route('/modifier_ligne/<int:id_ligne>', methods = ['PUT'])
def modifier_ligne(id_ligne):
    data = request.json
    new_libelle = data.get('new_libelle')
    new_id_agence = data.get('new_id_agence')
    if not new_libelle and new_id_agence is None:
         return jsonify({"Champs manquants": "Veuillez remplir tous les champs"})
    query = "SELECT libelle_ligne, id_agence FROM ligne WHERE id_ligne = %s"
    params = (id_ligne,)
    is_exist = execute_fetchone(query, params = params)
    if not is_exist:
         return jsonify({'error':'ligne not found'}), 404
    if new_id_agence is not None:
        try :
            new_id_agence = int(new_id_agence)
        except ValueError:
            return jsonify({"error":"id_agence must be a number"}),400
    if new_libelle:
        query = "UPDATE ligne SET libelle_ligne=%s WHERE id_ligne=%s"
        params = (new_libelle, id_ligne)
        try:
            execute_modifi(query, params = params)
            return jsonify({"message":"libel changed successfully"})
        except:
            return jsonify({"error":"modification not done due to a problem"})
    
    if new_id_agence and new_libelle:
        query = "UPDATE ligne SET libelle_ligne=%s, id_agence=%s WHERE id_ligne=%s"
        params = (new_libelle, new_id_agence, id_ligne)
        try:
            execute_modifi(query, params = params)
            return jsonify({"message":"libelle_ligne and id agence changed successfully"})
        except:
             return jsonify({"error":"modification not done due to a problem"})
    if new_id_agence:
        query = "UPDATE ligne SET id_agence=%s WHERE id_ligne=%s"
        params = (new_id_agence, id_ligne)
        try:
            execute_modifi(query, params = params)
            return jsonify({"message":"id agence changed successfully"})
        except:
            return jsonify({"error":"modification not done due to a problem"})

        
@gest_ligne_bp.route('/supprimer_ligne/<int:id_ligne>', methods = ['DELETE'])              
def supprimer_ligne(id_ligne):
    query = "SELECT new_libelle, id_agence FROM ligne WHERE id_ligne = %s"
    params = (id_ligne,)
    is_exist = execute_fetchone(query, params = params)
    if not is_exist:
         return jsonify({'error':'ligne not found'}), 404
    query = "DELETE FROM ligne WHERE id_ligne=%s"
    params = (id_ligne,)
    try:
        execute_modifi(query, params = params)
        return jsonify({"Succès":"Ligne supprimée !"})

    except Exception as e:
        return jsonify({"Erreur DB": str(e)})