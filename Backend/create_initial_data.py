from flask import current_app as app
from Backend.models import db
from flask_security import SQLAlchemyUserDatastore

with app.app_context():
    db.create_all()
    userdatastore : SQLAlchemyUserDatastore = app.security.datastore
    userdatastore.find_or_create_role(name='Admin', description='Administrator')
    userdatastore.find_or_create_role(name='User', description='User')
    
    if not userdatastore.find_user(username = 'aryan_admin'):
        userdatastore.create_user(
            username='aryan_admin', 
            password='admin123', 
            email='admin@gmail.com', 
            full_name='Admin_Aryan', 
            qualification='Admin', 
            roles=['Admin'])
    db.session.commit()
    print("Tables created successfully")
    