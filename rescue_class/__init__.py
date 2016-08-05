from flask import Flask
from flask_login import LoginManager


from rescue_class.utils import ReverseProxied
import requests


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

app.config.from_pyfile('config.py')
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message_category = 'warning'


import rescue_class.views
import rescue_class.models
