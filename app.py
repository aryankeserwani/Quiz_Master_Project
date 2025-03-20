from flask import Flask
from Backend.config import LocalDevelopmentConfig
from Backend.resources import api
from Backend.models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_cors import CORS

def createApp():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # models init
    db.init_app(app)
    
    api.init_app(app)
    
    # flask-security init
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore=datastore, register_blueprint=False)
    app.app_context().push()
    
    return app

app=createApp()

import Backend.create_initial_data
import Backend.routes

# Handle SPA routing - must be after the API routes are registered
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)