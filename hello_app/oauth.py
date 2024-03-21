import os
from . import app
from flask import redirect, url_for
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)

github = oauth.register(
    name='github',
    client_id=os.environ.get("GH_CLIENT_ID"),
    client_secret=os.environ.get("GH_SECRET_ID"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
) 

@oauth.route('/login')
def login():
    redirect_uri = url_for('oauth.authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@oauth.route('/callback')
def authorize():
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    return redirect(url_for('home'))


