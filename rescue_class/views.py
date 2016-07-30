# views.py
from flask import Flask, flash, redirect, url_for, session, render_template, request
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from oauth2client.client import OAuth2WebServerFlow

from oauth2client import client
from apiclient import discovery
import httplib2

from rescue_class import app, login_manager, models

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

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

    APP_ID = 'de68608c52e71e5f3669b53afdf1e26a1d460bb83f0ac736382c525b2e5dbe37'
    APP_SECRET = '4a8a8623c5a650e63562ec971f9d8e968280853bc92334e8f81591f6c74b4635'
    SCOPE = 'time_data focustime_data'
    BASE_URL = 'https://www.rescuetime.com/oauth/authorize?client_id=de68608c52e71e5f3669b53afdf1e26a1d460bb83f0ac736382c525b2e5dbe37'
    REDIRECT_URL = 'https://slm.smalldata.io/rescueOauth2Callback'
    AUTH_URL = '%(base_url)s&redirect_uri=%(redirect_url)s&response_type=code&scope=%(scope)s' % {
                    'base_url': BASE_URL,
                    'redirect_url': REDIRECT_URL,
                    'scope': SCOPE
                }

    flow = OAuth2WebServerFlow(
                           client_id = APP_ID,
                           client_secret = APP_SECRET,
                           scope = SCOPE,
                           redirect_uri = url_for('rescueOauth2Callback', _external=True))

    if 'code' not in request.args:
        return redirect(AUTH_URL)
    else:
        auth_code = request.args.get('code')
        print 'auth_code: %s' % auth_code


        url = 'https://www.rescuetime.com/oauth/token'
        data = {
            'client_id': APP_ID,
            'client_secret': APP_SECRET,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://slm.smalldata.io/rescueOauth2Callback'
        }

        r = requests.post(url, data=data)
        print 'r.status_code: %s' % r.status_code
        print 'r.text: %s' % r.text

        if r.status_code != 200:
            flash('RescueTime Error: ' + r.text, 'error')
        else:
            results = json.loads(r.text)
            current_user.update_field('rescuetime_access_token', results['access_token'])

            # fetch sample data
            url = 'https://www.rescuetime.com/api/oauth/daily_summary_feed'
            params = {'access_token': results['access_token']}
            r = requests.get(url, params=params)
            flash('RescueTime result: %s' % r.text[:100], 'success')
        return redirect(url_for('home'))



@login_manager.user_loader
def user_loader(user_id):
    return models.get_user(user_id)


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return render_template('logout.html')
