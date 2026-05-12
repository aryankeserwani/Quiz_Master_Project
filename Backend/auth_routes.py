from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_required, current_user
from Backend.models import db, user_datastore, User, Role

# Register a new user
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    
    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400
    
    # Check if user with the same email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User with this email already exists"}), 400
    
    # Create new user with Student role
    student_role = Role.query.filter_by(name="Student").first()
    if not student_role:
        return jsonify({"message": "Student role not found"}), 500
    
    new_user = user_datastore.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    
    user_datastore.add_role_to_user(new_user, student_role)
    db.session.commit()
    
    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }
    }), 201

# The login route is handled by Flask-Security-Too
# This is a custom route to provide additional user information upon successful login
@app.route("/api/login-info", methods=["GET"])
@auth_required("token")
def login_info():
    return jsonify({
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "roles": [role.name for role in current_user.roles],
        "active": current_user.active
    })

# Logout is handled by Flask-Security-Too
# This can be a custom route if needed
@app.route("/api/logout", methods=["POST"])
@auth_required("token")
def logout():
    # Flask-Security-Too handles the actual logout mechanism
    # This is just a placeholder to return a success response
    return jsonify({"message": "Logout successful"})

# Request password reset
@app.route("/api/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    
    if not email:
        return jsonify({"message": "Email is required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal whether a user exists for security reasons
        return jsonify({"message": "If your email is registered, you will receive a password reset link"}), 200
    
    # Here you would typically:
    # 1. Generate a reset token
    # 2. Send an email with a link containing the token
    # 3. Save the token in the database with an expiration time
    
    # For simplicity in this example, we'll just return a success message
    # In a real application, you would implement the full flow
    
    return jsonify({
        "message": "If your email is registered, you will receive a password reset link"
    }), 200

# Reset password using token
@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    
    token = data.get("token")
    new_password = data.get("new_password")
    
    if not token or not new_password:
        return jsonify({
            "message": "Token and new password are required"
        }), 400
    
    # In a real application, you would:
    # 1. Verify the token is valid and not expired
    # 2. Find the user associated with the token
    # 3. Update their password
    # 4. Invalidate the token
    
    # For simplicity in this example, we'll just return a success message
    # In a real application, you would implement the full flow
    
    return jsonify({
        "message": "Password has been reset successfully"
    }), 200 