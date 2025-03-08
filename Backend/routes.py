from flask import current_app as app, jsonify, render_template, request
from flask_security import auth_required, roles_required, current_user, verify_password, hash_password
from Backend.models import db
datastore = app.security.datastore

@app.get("/")
def hello():
    return render_template('index.html')

@app.get("/protected")
@auth_required('token')
def protected():
    return '<h1>Only accesible by auth User</h1>'

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    user = datastore.find_user(username = username)
    
    if not user:
        return jsonify({"message": "Please enter valid username and password"}), 400
    
    if verify_password(password, user.password):
        return jsonify({"token": user.get_auth_token(),"username": user.username, "email": user.email, "role": user.roles[0].name, "id": user.id})
    
    return jsonify({"message": "Please enter valid username and password"})

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    email = data.get('email')
    fullname = data.get('fullname')
    qualification = data.get('qualification')
    dob = data.get('dob')
    
    if not username or not password  or role not in ['admin', 'user']:
        return jsonify({"message": "Invalid credentials"}), 404
    
    user = datastore.find_user(username = username)
    
    if user:
        return jsonify({"message": "Username already exists"}), 404
    
    try:
        datastore.create_user(username = username, password = hash_password(password), roles = [role], full_name = fullname, qualification = qualification, dob = dob, email = email, active = True )
        db.session.commit()
        return jsonify({"message": "User is successfully registered"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "Error in registering"}), 400
    
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