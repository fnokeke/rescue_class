from flask import Flask, flash, redirect, url_for, session, render_template, request
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

from rescue_class.utils import ReverseProxied


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

app.config.from_pyfile('config.py')
login_manager = LoginManager(app)


import rescue_class.views
import rescue_class.models
