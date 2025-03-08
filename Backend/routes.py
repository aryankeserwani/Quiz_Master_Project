from flask import current_app as app, jsonify, render_template, request
from flask_security import auth_required, roles_required, current_user, verify_password, hash_password
from Backend.models import db, User, Role
from datetime import datetime

userdatastore = app.security.datastore

@app.get("/")
def hello():
    return render_template('index.html')

@app.get("/protected")
@auth_required('token')
def protected():
    return '<h1>Only accesible by auth User</h1>'

@app.route("/api/login", methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    user = userdatastore.find_user(username = username)
    
    if not user:
        return jsonify({"message": "Please enter valid username and password"}), 400
    
    if verify_password(password, user.password):
        return jsonify({"token": user.get_auth_token(),
        "username": user.username,
         "email": user.email,
         "role": user.roles[0].name,
         "id": user.id})
    
    return jsonify({"message": "Please enter valid username and password"})

@app.route("/api/register", methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    fullname = data.get('fullname')
    qualification = data.get('qualification')
    dob_str = data.get('dob')  # Get the string from the request
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()  # Convert to date object
    if not username or not password:
        return jsonify({"message": "Invalid credentials"}), 404
    
    user = userdatastore.find_user(username = username)
    if user:
        return jsonify({"message": "Username already exists!"}), 404
    
    userdatastore.create_user(username = username,
        password = hash_password(password),
        roles = ['user'],
        full_name = fullname,
        qualification = qualification,
        dob = dob,
        email = email,
        active = True )
    db.session.commit()
    return jsonify({"message": "User is successfully registered"}), 201
   
    
@app.route("/api/admin")
@auth_required('token')
@roles_required('Admin')
def admin_home():
    return jsonify({"message": "Welcome Admin"})   

@app.route("/api/user_dashboard")
@auth_required('token')
@roles_required('user')
def user_home():
    user = current_user
    return jsonify({
        "username": user.username,
        "password": user.password,
        "email": user.email
    })