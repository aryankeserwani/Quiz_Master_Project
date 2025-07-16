from flask import Flask
from Backend.config import LocalDevelopmentConfig
from Backend.resources import api
from Backend.models import db, User
from Backend.security import jwt
from flask_cors import CORS

def createApp():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # models init
    db.init_app(app)
    
    api.init_app(app)
    
    # flask-jwt init
    jwt.init_app(app)
    app.app_context().push()
    
    return app

app=createApp()


from Backend.routes import *

# Handle SPA routing - must be after the API routes are registered
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    # # Only add admin if not already present
    # if not User.query.filter_by(username="aryan_admin").first():
    #     db.create_all()
    #     db.session.add(User(
    #         username="aryan_admin",
    #         email="admin@gmail.com",
    #         password=generate_password_hash("admin123"),
    #         fullname="Admin",
    #         qualification="Admin",
    #         role="Admin"
    #     ))
    #     db.session.commit()
    app.run(host='0.0.0.0', port=5000)