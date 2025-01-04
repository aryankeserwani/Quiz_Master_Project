class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DEBUG=False
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI='sqlite:///quiz_master.db'
    DEBUG=True
    SECURITY_PASSWORD_HASH='bcrypt'
    SECURITY_PASSWORD_SALT='thisisasecret'
    SECRET_KEY="295dcf416690cbf5b76d34ac146361adec39a2fcb74055f0df7a6d7fb81d8aa029374356c1b6bcf7bd22e32f6d68141c82bce960d85525373bb83d8bbdb9d5c"
    WTF_CSRF_ENABLED=False