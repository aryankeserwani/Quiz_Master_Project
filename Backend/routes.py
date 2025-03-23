# Import necessary modules and libraries
from flask import current_app as app, jsonify, render_template, request
from flask_security import (
    auth_required,
    roles_required,
    current_user,
    verify_password,
    hash_password,
)
from Backend.models import db, User, Role
from datetime import datetime

# Initialize the user datastore for managing user data
userdatastore = app.security.datastore

# Route to serve the main index.html file
@app.get("/")
def hello():
    return app.send_static_file("index.html")

# Protected route accessible only by authenticated users
@app.get("/protected")
@auth_required("token")
def protected():
    return "<h1>Only accesible by auth User</h1>"

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

    # Find the user in the datastore
    user = userdatastore.find_user(username=username)

    # Check if user exists and password is correct
    if not user:
        return jsonify({"message": "Please enter valid username and password"}), 400

    if verify_password(password, user.password):
        # Return user details and authentication token
        return jsonify(
            {
                "token": user.get_auth_token(),
                "username": user.username,
                "email": user.email,
                "role": user.roles[0].name,
                "id": user.id,
            }
        )

    # Return error if authentication fails
    return jsonify({"message": "Please enter valid username and password"})

# API endpoint for user registration
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
        return jsonify({"message": "Invalid credentials"}), 404

    # Check if the username already exists
    user = userdatastore.find_user(username=username)
    if user:
        return jsonify({"message": "Username already exists!"}), 404

    # Get or create the user role
    user_role = userdatastore.find_role("user")
    if not user_role:
        # Create the role if it doesn't exist
        user_role = userdatastore.create_role(name="user", description="User")
        db.session.commit()  # Commit the role creation to the database

    # Create a new user with the provided details
    userdatastore.create_user(
        username=username,
        password=hash_password(password),
        roles=[user_role],
        full_name=fullname,
        qualification=qualification,
        dob=dob,
        email=email,
        active=True,
    )
    db.session.commit()  # Commit the changes to the database
    return jsonify({"message": "User is successfully registered"}), 201

# Admin-only route, accessible by users with the "Admin" role
@app.route("/api/admin")
@auth_required("token")
@roles_required("Admin")
def admin_home():
    return jsonify({"message": "Welcome Admin"})

# User dashboard route, accessible by users with the "user" role
@app.route("/api/user_dashboard")
@auth_required("token")
@roles_required("user")
def user_home():
    user = current_user  # Get the current authenticated user
    return jsonify(
        {"username": user.username, "password": user.password, "email": user.email}
    )