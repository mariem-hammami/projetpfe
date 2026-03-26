from flask import Flask
from db.database import connect_db
from services.auth import auth_bp
from routes.gestion_lignes import gest_ligne_bp
from routes.gestion_bus import gest_bus_bp
app = Flask(__name__)


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(gest_ligne_bp, url_prefix='/gest_ligne')
app.register_blueprint(gest_bus_bp, url_prefix = '/gest_bus')

if __name__ == "__main__":
    app.run(debug=True)
