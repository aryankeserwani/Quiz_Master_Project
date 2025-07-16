# Import necessary modules and libraries
from flask import current_app as app, jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from Backend.models import db, User
from datetime import datetime
from functools import wraps

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != role:
                return jsonify(message = "You are not authorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# Route to serve the main index.html file
@app.get("/")
def hello():
    return app.send_static_file("index.html")

# API endpoint for user login

@app.route("/api/login", methods=["POST"])
def login():
    # Parse JSON data from the request
    data = request.get_json()

    # Extract username and password from the request
    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Find the user by username
    user = User.query.filter_by(username=username).one_or_none()

    # Check if user exists and password is correct
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Wrong username and password"}), 401
    
    access_token = create_access_token(identity=user)
    return jsonify(
        access_token=access_token,
        message="Login successfull"
    ), 200


# # API endpoint for user registration
@app.route("/api/register", methods=["POST"])
def register():
    # Parse JSON data from the request
    data = request.get_json()

    # Extract user details from the request
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    fullname = data.get("fullname")
    qualification = data.get("qualification")
    dob_str = data.get("dob")  # Get the string from the request
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()  # Convert to date object

    # Validate input
    if not username or not password:
        return jsonify({"message": "Invalid credentials"}), 400

    # Check if the username already exists
    user = User.query.filter_by(username=username).one_or_none()
    if user:
        return jsonify({"message": "Username already exists!"}), 400

    # Create a new user with the provided details
    user = User(
        username=username,
        password=generate_password_hash(password),
        fullname=fullname,
        qualification=qualification,
        dob=dob,
        email=email,
        active=True,
    )
    db.session.add(user)  # Add the user to the session
    db.session.commit()  # Commit the changes to the database
    return jsonify({"message": "User is successfully registered"}), 200

# # Admin-only route, accessible by users with the "Admin" role
@app.route("/api/admin")
@role_required("Admin")
def admin_home():
    return jsonify({"message": "Welcome Admin"})

# # User dashboard route, accessible by users with the "user" role
@app.route("/api/user_dashboard")

def user_home():
    user = current_user  # Get the current authenticated user
    return jsonify(
        {"username": user.username, "password": user.password, "email": user.email}
    )