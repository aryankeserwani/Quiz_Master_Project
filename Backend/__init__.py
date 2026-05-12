from flask import Flask, jsonify
from flask_cors import CORS
from flask_security import Security, hash_password
from Backend.models import db, user_datastore
import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Allow CORS for frontend
    CORS(app, supports_credentials=True)
    
    if test_config is None:
        # Load configuration from config.py
        app.config.from_object('Backend.config.DevelopmentConfig')
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Initialize database
    db.init_app(app)
    
    # Setup Flask-Security
    security = Security(app, user_datastore)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
        # Create roles if they don't exist
        if not user_datastore.find_role('Admin'):
            user_datastore.create_role(name='Admin', description='Administrator')
        
        if not user_datastore.find_role('Student'):
            user_datastore.create_role(name='Student', description='Student')
        
        # Create admin user if it doesn't exist
        if not user_datastore.find_user(email='admin@example.com'):
            user_datastore.create_user(
                email='admin@example.com',
                password=hash_password('password'),
                first_name='Admin',
                last_name='User',
                roles=['Admin']
            )
        
        # Commit changes
        db.session.commit()
    
    # Import route modules
    with app.app_context():
        # Import route modules here to avoid circular imports
        import Backend.auth_routes
        import Backend.user_routes
        import Backend.subject_chapter_routes
        import Backend.quiz_routes
        import Backend.score_routes
        
        # Define a simple route for testing
        @app.route('/')
        def index():
            return jsonify({'message': 'Welcome to Quiz Master API!'})
        
        # Error handlers
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({'message': 'Resource not found'}), 404
        
        @app.errorhandler(500)
        def server_error(error):
            return jsonify({'message': 'Server error'}), 500
    
    return app 