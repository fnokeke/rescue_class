# views.py
from flask import Flask, flash, redirect, url_for, session, render_template, request
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from oauth2client.client import OAuth2WebServerFlow

from oauth2client import client
from apiclient import discovery

import httplib2
import requests
import json

from rescue_class import app, login_manager, models


class RescueOauth2:

    APP_ID = app.config['RT_APP_ID']
    APP_SECRET = app.config['RT_APP_SECRET']
    SCOPE = 'time_data focustime_data'
    BASE_URL = app.config['RT_BASE_URL']

    def __init__(self):
        self.redirect_url = url_for('rescueOauth2Callback', _external=True)
        self.auth_url = '%(base_url)s&redirect_uri=%(redirect_url)s&response_type=code&scope=%(scope)s' % {
                            'base_url': self.BASE_URL,
                            'redirect_url': self.redirect_url,
                            'scope': self.SCOPE
                         }

        self.flow = OAuth2WebServerFlow(
                           client_id = self.APP_ID,
                           client_secret = self.APP_SECRET,
                           scope = self.SCOPE,
                           redirect_uri = self.redirect_url)


    def fetch_token(self, user, code):
        if not code:
            raise ValueError("Invalid request code in set_access_token")

        url = 'https://www.rescuetime.com/oauth/token'
        data = {
            'client_id': self.APP_ID,
            'client_secret': self.APP_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_url
        }

        r = requests.post(url, data=data)
        if r.status_code == 200:
            results = json.loads(r.text)
            self.token = results['access_token']
            user.update_field('access_token', self.token)
            print 'user.access_token: %s' % user.access_token

        return r.status_code, r.text


    def fetch_daily_summary(self, user):
        url = 'https://www.rescuetime.com/api/oauth/daily_summary_feed'
        params = {'access_token': user.access_token}
        r = requests.get(url, params=params)
        return r.status_code, r.text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    rt = RescueOauth2()
    status, results = rt.fetch_daily_summary(current_user)
    ctx = {
        'users': models.get_all_users(),
        'results': json.loads(results)
    }
    return render_template('dashboard.html', **ctx)


@app.route('/oauth2callback')
def oauth2callback():
    flow = OAuth2WebServerFlow(client_id= app.config['GOOGLE_CLIENT_ID'],
                           client_secret= app.config['GOOGLE_CLIENT_SECRET'],
                           scope= app.config['GOOGLE_SCOPE'],
                           redirect_uri=url_for('oauth2callback', _external=True))

    auth_code = request.args.get('code')
    if not auth_code:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)

    credentials = flow.step2_exchange(auth_code, http=httplib2.Http())
    if credentials.access_token_expired:
        credentials.refresh(httplib2.Http())

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('oauth2', 'v2', http=http)

    userinfo = service.userinfo().get().execute()
    user = models.create_user(userinfo)
    login_user(user)
    return redirect(url_for('index'))


@app.route('/rescueOauth2Callback')
def rescueOauth2Callback():
    if 'error' in request.args:
        flash('Sorry user did not grant authentication :(', 'error')
        return redirect(url_for('home'))

    rt = RescueOauth2()
    if 'code' not in request.args:
        return redirect(rt.auth_url)

    code = request.args.get('code')
    status, result = rt.fetch_token(current_user, code)

    msg, category = ('Successfully connected to your RescueTime account.', 'success'
                    ) if status == 200 else ('Connection error. Try again.', 'warning')
    flash(msg, category)
    return render_template('index.html')

@login_manager.user_loader
def user_loader(user_id):
    return models.get_user(user_id)


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return render_template('logout.html')
