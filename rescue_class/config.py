# config.py
from rescue_class import secret_keys

SECRET_KEY = secret_keys.SECRET_KEY
SESSION_TYPE = 'redis'

SQLALCHEMY_DATABASE_URI = secret_keys.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

GOOGLE_CLIENT_ID = secret_keys.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = secret_keys.GOOGLE_CLIENT_SECRET
GOOGLE_SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
