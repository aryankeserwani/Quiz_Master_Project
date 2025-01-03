class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DEBUG=False
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI='sqlite:///quiz_master.db'
    DEBUG=True
    SECURITY_PASSWORD_HASH='bcrypt'
    SECURITY_PASSWORD_SALT='thisisasecret'