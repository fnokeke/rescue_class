# config.py
from rescue_class import secret_keys

SECRET_KEY = secret_keys.SECRET_KEY
SESSION_TYPE = 'redis'

SQLALCHEMY_DATABASE_URI = secret_keys.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

GOOGLE_CLIENT_ID = secret_keys.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = secret_keys.GOOGLE_CLIENT_SECRET
GOOGLE_SCOPE = 'https://www.googleapis.com/auth/userinfo.email'

RT_APP_ID = secret_keys.RT_APP_ID
RT_APP_SECRET = secret_keys.RT_APP_SECRET
RT_CLIENT_ID = secret_keys.RT_CLIENT_ID
RT_BASE_URL = 'https://www.rescuetime.com/oauth/authorize?client_id=' + RT_CLIENT_ID
