# auth.py
from flask import Blueprint, session, redirect, url_for, request
from authlib.integrations.flask_client import OAuth
import os
import requests
from .dbconnect import dbsession
from .models import Account
import secrets
from . import app

oauth_bp = Blueprint('oauth', __name__)

oauth = OAuth()
# registrering af github oauth klienten
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

@oauth_bp.route('/login')
def register():
   github = oauth.create_client('github')
   redirect_uri = url_for('oauth.authorize', _external=True)
   app.logger.info(f"Redirecting to: {redirect_uri}")
   print(f"Redirecting to: {redirect_uri}")
   return github.authorize_redirect(redirect_uri)

@oauth_bp.route('/authorize')
def authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    profile = resp.json()

    user = dbsession.query(Account).filter_by(username=profile['login']).first()

    if user is None:
        user = Account(username=profile['login'], password=secrets.token_urlsafe(32), email=profile.get('email',profile['login']), roleID=1)
        dbsession.add(user)
        dbsession.commit()
    session['userID'] = user.accountID
    session['user'] = user.username
    session['userEmail'] = user.email
    session['roleID'] = user.roleID
    session['oauth'] = 'github'
    session['oauth_id'] = profile['id']
    session['oauth_token_type'] = token['token_type']
    session['oauth_token'] = token['access_token']

    return redirect('/')

@oauth_bp.route('/logout')
def logout():
    # Her antager vi at client_id og client_secret er sat op som globale variabler eller hentes fra et sikkert sted
    revoke_github_token(session['oauth_token'], os.environ.get("GH_CLIENT_ID"), os.environ.get("GH_SECRET_ID"))
    session.clear()
    return redirect('/')

def revoke_github_token(access_token, client_id, client_secret):

    url = f'https://api.github.com/applications/{client_id}/token'
    response = requests.delete(
        url,
        params={'access_token': access_token},
        auth=(client_id, client_secret)
    )
    if response.status_code == 204:
        print("Token successfully revoked.")
    else:
        print("Failed to revoke token.")
