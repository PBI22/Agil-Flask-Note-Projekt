import os
from . import app
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)

github = oauth.register(
    name='github',
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("SECRET_ID"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)  