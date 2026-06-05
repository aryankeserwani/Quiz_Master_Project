import os
from datetime import timedelta

class Config:
    # Flask configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
<<<<<<< HEAD
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///instance/quiz_master.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Security configuration
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'dev-salt-change-in-production')
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = 86400  # 24 hours
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = False  # We'll handle registration ourselves
    SECURITY_RECOVERABLE = False  # We'll handle password reset ourselves
    SECURITY_CHANGEABLE = False  # We'll handle password change ourselves
    SECURITY_SEND_REGISTER_EMAIL = False
=======
    # config for security
    JWT_SECRET_KEY=''
    SECURITY_PASSWORD_HASH='bcrypt'
    SECURITY_PASSWORD_SALT='thisisasecret'
>>>>>>> 
    
    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'


class DevelopmentConfig(Config):
    DEBUG = True
    # Additional development-specific settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)  # Longer token for development


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    

class ProductionConfig(Config):
    # Production-specific settings
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')  # Must be set in production
    
    # Database configuration for production (e.g., PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/quiz_master')
    
    # Security headers
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
