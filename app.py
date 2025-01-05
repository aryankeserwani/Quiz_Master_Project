from flask import Flask
from Backend.config import LocalDevelopmentConfig
from Backend.models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore, auth_required

def createApp():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # models init
    db.init_app(app)
    
    #flask-security init
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore=datastore, register_blueprint=False)
    app.app_context().push()
    
    return app

app=createApp()
import Backend.create_initial_data

@app.get("/")
def hello():
    return '<h1>Hello World</h1>'

if __name__ == "__main__":
    app.run()