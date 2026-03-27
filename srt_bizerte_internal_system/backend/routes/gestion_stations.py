from flask import Flask, request, jsonify, Blueprint
from db.database import connect_db, execute_fetchall, execute_fetchone, execute_modifi

gest_station_bp = Blueprint("/gest_station", __name__)

@gest_station_bp.route('/get_station', methods = ['GET'])
def load_stations():
    try:
        query = """
            SELECT s.id_station, s.libelle_station, s.latitude, s.longitude,
                        l.libelle_ligne, ls.ordre
                FROM station s
                LEFT JOIN ligne_station ls ON s.id_station = ls.id_station
                LEFT JOIN ligne l ON ls.id_ligne = l.id_ligne
                ORDER BY l.libelle_ligne, ls.ordre
            """
        rows = execute_fetchall(query)
        stations = []
        for r in rows:
            stations.append({"station_id":r[0],
                             "libellle_station": r[1],
                             "latitude":r[2],
                             "logitude":r[3],
                             "libelle_ligne":r[4],
                             'ordre':r[5]})
        return jsonify(stations)
    except Exception as e:
        return jsonify({"Erreur DB": str(e)})
    
@gest_station_bp.route('/ajouter_station_into_ligne', methods = ['POST'])
def ajouter_station_into_ligne():
    data = request.json
    libelle = data.get("Libellé_station")
    latitude = data.get("Latitude")
    longitude = data.get("Longitude")
    id_ligne = data.get('id_ligne')
    ordre = data.get("ordre")
    if not libelle  and not latitude and not longitude and not id_ligne:
        return jsonify({"error":"missing information"})
    try:
        query = "SELECT id_ligne, libelle_ligne FROM ligne WHERE id_ligne = %s"
        params = (id_ligne,)

        ligne = execute_fetchone(query, params = params)
        if not ligne:
            return jsonify({"error": "ligne not found."})
        query = "INSERT INTO station (libelle_station, latitude, longitude) VALUES (%s,%s,%s)"
        params = (libelle, latitude, longitude)
        id_station = execute_modifi(query, params = params)
        query = "SELECT MAX(ordre) FROM ligne_station WHERE id_ligne=%s"
        params = (id_ligne,)
        max_ordre = execute_fetchone(query, params = params)
        if ordre:
            if max_ordre:
                max_ordre = max_ordre[0]
                if ordre == max_ordre+1:
                    execute_modifi("INSERT INTO ligne_station (id_ligne, id_station, ordre) VALUES (%s,%s,%s)", 
                        params = (id_ligne, id_station, ordre))
                elif ordre <= max_ordre:
                    for i in range(ordre+1,int(max_ordre)+1,1):
                        query = "UPDATE ligne_station SET ordre = ordre + 1  WHERE id_ligne != %s AND ordre = %s and id_station = %s"
                        params = (id_ligne, i, id_station)
                else:
                    return jsonify ({"error": "invalide error"})
            else :
                ordre = 1
                execute_modifi("INSERT INTO ligne_station (id_ligne, id_station, ordre) VALUES (%s,%s,%s)", 
                               params = (id_ligne, id_station, ordre))
        return jsonify ({"Succès": "Station ajoutée !"})
    except Exception as e:
        return jsonify({"Erreur DB": str(e)})

@gest_station_bp.route('/modifier_station/<int:id_station>', methods = ['PUT'])
def modifier_station(id_station):
    data = request.json
    new_libelle = data.get("Libellé")
    new_lat = data.get("Latitude")
    new_long = data.get("Longitude")
    

    if not new_libelle and not new_lat and not new_long:
        return jsonify({"error":"enter at least a value to update"})
    try:
        query = "SELECT libelle_station, latitude, longitude FROM station WHERE id_station = %s"
        params = (id_station,)
        row = execute_fetchone(query, params = params)
        if row:
            if not new_libelle :
                new_libelle = row[0]
            if not new_lat:
                new_lat = row[1]
            if not new_long:
                new_long = row[2]
        else:
            return jsonify({"error":"station not found"}),400
        query = "SELECT libelle_station FROM station WHERE libelle_station = %s AND latitude = %s AND longitude = %s"
        params = (new_libelle,new_lat, new_long)
        is_exist = execute_fetchone(query, params = params)
        if is_exist:
            return jsonify({"message":"update faild due to existing value with the same info"})
        execute_modifi("UPDATE station SET libelle_station=%s, latitude=%s, longitude=%s WHERE id_station=%s",
                        params = (new_libelle, new_lat, new_long, id_station))
        return jsonify({"Succès": "Station modifiée !"})
    except Exception as e:
        return jsonify({"Erreur DB": str(e)}), 400

@gest_station_bp.route('/supprimer_station/<int:id_station>', methods = ['DELETE'])
def supprimer_station(id_station):
    query = "SELECT id_station FROM station WHERE id_station = %s"
    is_exists = execute_fetchone(query, params = (id_station,))
    if not is_exists:
        return jsonify({"error":"row not found"}), 400
    try:
        execute_modifi("DELETE FROM trajet WHERE  station_arrivee = %s", (id_station,))
        execute_modifi("DELETE FROM ligne_station WHERE id_station=%s", (id_station,))
        execute_modifi("DELETE FROM station WHERE id_station=%s", (id_station,)) 
        return jsonify({"Succès": "Station supprimée !"})
    except Exception as e:
        return jsonify({"Erreur DB": str(e)}),400