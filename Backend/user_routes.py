from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_required, current_user
from Backend.models import db, user_datastore, User, Role

# Get current user profile
@app.route("/api/users/me", methods=["GET"])
@auth_required("token")
def get_current_user():
    return jsonify({
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "roles": [role.name for role in current_user.roles],
        "active": current_user.active
    })

# Update current user profile
@app.route("/api/users/me", methods=["PUT"])
@auth_required("token")
def update_current_user():
    data = request.get_json()
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    
    if first_name:
        current_user.first_name = first_name
    
    if last_name:
        current_user.last_name = last_name
    
    db.session.commit()
    
    return jsonify({
        "message": "Profile updated successfully",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "roles": [role.name for role in current_user.roles],
            "active": current_user.active
        }
    })

# Change password
@app.route("/api/users/me/password", methods=["PUT"])
@auth_required("token")
def change_password():
    data = request.get_json()
    
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    
    if not current_password or not new_password:
        return jsonify({
            "message": "Current password and new password are required"
        }), 400
    
    # Verify current password
    if not user_datastore.verify_and_update_password(current_password, current_user):
        return jsonify({"message": "Current password is incorrect"}), 400
    
    # Update password
    user_datastore.change_user_password(current_user, new_password)
    db.session.commit()
    
    return jsonify({"message": "Password changed successfully"})

# Admin routes for user management
# Get all users (admin only)
@app.route("/api/users", methods=["GET"])
@auth_required("token")
@roles_required("Admin")
def get_all_users():
    users = User.query.all()
    result = []
    
    for user in users:
        result.append({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "roles": [role.name for role in user.roles],
            "active": user.active
        })
    
    return jsonify(result)

# Get a specific user (admin only)
@app.route("/api/users/<int:user_id>", methods=["GET"])
@auth_required("token")
@roles_required("Admin")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "roles": [role.name for role in user.roles],
        "active": user.active
    })

# Create a new user (admin only)
@app.route("/api/users", methods=["POST"])
@auth_required("token")
@roles_required("Admin")
def create_user():
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    roles = data.get("roles", ["Student"])  # Default role is Student
    
    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400
    
    # Check if user with the same email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User with this email already exists"}), 400
    
    # Create new user
    new_user = user_datastore.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    
    # Assign roles
    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if role:
            user_datastore.add_role_to_user(new_user, role)
    
    db.session.commit()
    
    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "roles": [role.name for role in new_user.roles],
            "active": new_user.active
        }
    }), 201

# Update a user (admin only)
@app.route("/api/users/<int:user_id>", methods=["PUT"])
@auth_required("token")
@roles_required("Admin")
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    active = data.get("active")
    roles = data.get("roles")
    
    if email:
        # Check if another user with the same email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"message": "User with this email already exists"}), 400
        
        user.email = email
    
    if first_name is not None:
        user.first_name = first_name
    
    if last_name is not None:
        user.last_name = last_name
    
    if active is not None:
        user.active = active
    
    if roles:
        # Clear existing roles
        for role in user.roles:
            user_datastore.remove_role_from_user(user, role)
        
        # Assign new roles
        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if role:
                user_datastore.add_role_to_user(user, role)
    
    db.session.commit()
    
    return jsonify({
        "message": "User updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "roles": [role.name for role in user.roles],
            "active": user.active
        }
    })

# Delete a user (admin only)
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("Admin")
def delete_user(user_id):
    if user_id == current_user.id:
        return jsonify({"message": "Cannot delete your own account"}), 400
    
    user = User.query.get_or_404(user_id)
    user_datastore.delete_user(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"})

# Reset a user's password (admin only)
@app.route("/api/users/<int:user_id>/reset-password", methods=["POST"])
@auth_required("token")
@roles_required("Admin")
def reset_user_password(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    new_password = data.get("new_password")
    
    if not new_password:
        return jsonify({"message": "New password is required"}), 400
    
    # Update password
    user_datastore.change_user_password(user, new_password)
    db.session.commit()
    
    return jsonify({"message": "Password reset successfully"}) 